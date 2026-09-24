from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CLASSMATE — AI Classroom Companion</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #090d16;
            color: #e6edf3;
            margin: 0;
            padding: 2rem;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 90vh;
        }
        .card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 2.5rem;
            max-width: 640px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        }
        h1 { color: #58a6ff; margin-top: 0; font-size: 1.8rem; }
        p { line-height: 1.6; color: #8b949e; }
        .badge {
            display: inline-block;
            background: #238636;
            color: #ffffff;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        .info-box {
            background: #0d1117;
            border-left: 4px solid #1f6feb;
            padding: 1rem;
            margin: 1.5rem 0;
            border-radius: 4px;
        }
        a.btn {
            display: inline-block;
            background: #238636;
            color: white;
            padding: 10px 20px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 1rem;
        }
        a.btn:hover { background: #2ea043; }
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">Vercel Deployment Status: Active</span>
        <h1>🎓 CLASSMATE</h1>
        <p>AI-Powered Classroom Accessibility Companion for Deaf & Hard-of-Hearing Students.</p>
        
        <div class="info-box">
            <strong style="color: #c9d1d9;">Architecture Note:</strong><br>
            CLASSMATE utilizes a full Streamlit interface with live WebSockets, Faster-Whisper speech recognition, acoustic sound classification, and local serial hardware triggers.
        </div>

        <p>To run the full interactive Streamlit application with live microphone audio transcription and serial hardware control:</p>
        <ul>
            <li><strong>Local:</strong> Run <code>streamlit run app.py</code> in your workspace.</li>
            <li><strong>Cloud Hosting:</strong> Deploy to <a href="https://share.streamlit.io" style="color: #58a6ff;" target="_blank">Streamlit Community Cloud</a> directly from GitHub.</li>
        </ul>

        <a href="https://github.com/Jeeva0107/CLASSMATE" target="_blank" class="btn">View GitHub Repository</a>
    </div>
</body>
</html>"""
        self.wfile.write(html.encode('utf-8'))
        return

app = handler
