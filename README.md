Flask Microtools – URL Shortener & Pastebin

This is a simple Flask-based backend project with a basic HTML frontend.

*   URL Shortener: Input a long URL, get a short link.
    
*   Pastebin: Submit text snippets with expiry time.
    

How to Run:

1.  Install dependencies:pip install -r requirements.txt
    
2.  Start the server:python app.py
    
3.  Open your browser and go to:[http://localhost:5000](http://localhost:5000)
    

Project Structure:

*   app.py → Flask backend logic
    
*   requirements.txt → Python dependencies
    
*   .gitignore → Files ignored by Git
    
*   static/index.html → Frontend HTML
    

Sample API Usage:

POST /shortenBody: { "url": "[https://example.com](https://example.com)" }

POST /pasteBody: { "content": "Hello world", "expiry": 3600 }
