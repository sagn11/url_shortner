from flask import Flask, request, redirect, jsonify
import hashlib
import sqlite3
import time

app = Flask(__name__, static_folder='static')

conn = sqlite3.connect('project.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS url_map (
    id INTEGER PRIMARY KEY,
    original_url TEXT,
    short_code TEXT UNIQUE,
    clicks INTEGER
)''')

c.execute('''CREATE TABLE IF NOT EXISTS pastes (
    id INTEGER PRIMARY KEY,
    content TEXT,
    paste_id TEXT UNIQUE,
    expiry INTEGER
)''')

conn.commit()

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    original_url = data.get('url')
    if not original_url:
        return jsonify({'error': 'No URL provided'}), 400

    short_code = hashlib.md5(original_url.encode()).hexdigest()[:6]
    c.execute("INSERT OR IGNORE INTO url_map (original_url, short_code, clicks) VALUES (?, ?, 0)",
              (original_url, short_code))
    conn.commit()
    return jsonify({'short_url': request.host_url + 'u/' + short_code})

@app.route('/u/<short_code>')
def redirect_url(short_code):
    c.execute("SELECT original_url, clicks FROM url_map WHERE short_code = ?", (short_code,))
    row = c.fetchone()
    if row:
        c.execute("UPDATE url_map SET clicks = ? WHERE short_code = ?", (row[1]+1, short_code))
        conn.commit()
        return redirect(row[0])
    return jsonify({'error': 'URL not found'}), 404

@app.route('/paste', methods=['POST'])
def create_paste():
    data = request.get_json()
    content = data.get('content')
    expiry = int(data.get('expiry', 3600))
    if not content:
        return jsonify({'error': 'No content provided'}), 400

    paste_id = hashlib.sha1(content.encode()).hexdigest()[:8]
    expire_at = int(time.time()) + expiry
    c.execute("INSERT OR REPLACE INTO pastes (content, paste_id, expiry) VALUES (?, ?, ?)",
              (content, paste_id, expire_at))
    conn.commit()
    return jsonify({'paste_url': request.host_url + 'paste/' + paste_id})

@app.route('/paste/<paste_id>')
def get_paste(paste_id):
    now = int(time.time())
    c.execute("SELECT content, expiry FROM pastes WHERE paste_id = ?", (paste_id,))
    row = c.fetchone()
    if row:
        if row[1] >= now:
            return jsonify({'content': row[0]})
        else:
            return jsonify({'error': 'Paste expired'}), 410
    return jsonify({'error': 'Paste not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)