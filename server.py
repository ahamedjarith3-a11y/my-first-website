"""J&J Construction - dependency-free web app with SQLite persistence."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import os
from pathlib import Path
import json, sqlite3, time

ROOT = Path(__file__).parent
DB = Path(os.environ.get("DATABASE_PATH", str(ROOT / "jj_construction.db")))

PROJECTS = [
    {"title": "Bayview Residence", "location": "Chennai, TN", "type": "Residential", "year": "2025", "image": "residence", "description": "A light-filled coastal home built for everyday living."},
    {"title": "The Foundry Offices", "location": "Bengaluru, KA", "type": "Commercial", "year": "2024", "image": "office", "description": "Adaptive workplace renovation with warm industrial character."},
    {"title": "Aster Courtyard", "location": "Coimbatore, TN", "type": "Hospitality", "year": "2024", "image": "courtyard", "description": "A calm boutique stay shaped around an open garden court."}
]

def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS inquiries (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT, project_type TEXT, message TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
    con.commit(); con.close()

class App(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs): super().__init__(*args, directory=str(ROOT), **kwargs)
    def send_json(self, data, status=200):
        raw = json.dumps(data).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        if self.path == '/api/projects': return self.send_json(PROJECTS)
        if self.path == '/api/health': return self.send_json({"status":"ok", "service":"J&J Construction", "time":int(time.time())})
        return super().do_GET()
    def do_POST(self):
        if self.path != '/api/inquiries': return self.send_json({"error":"Not found"},404)
        try:
            size=int(self.headers.get('Content-Length','0')); data=json.loads(self.rfile.read(size))
            required = ['name','email','message']
            if not all(str(data.get(k,'')).strip() for k in required): return self.send_json({"error":"Please complete the required fields."},400)
            con=sqlite3.connect(DB); con.execute("INSERT INTO inquiries(name,email,phone,project_type,message) VALUES(?,?,?,?,?)",(data['name'].strip(),data['email'].strip(),data.get('phone','').strip(),data.get('projectType','').strip(),data['message'].strip())); con.commit(); con.close()
            return self.send_json({"message":"Thanks — your project enquiry is on its way."},201)
        except (json.JSONDecodeError, ValueError): return self.send_json({"error":"Invalid request."},400)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8080'))
    init_db(); print(f'J&J Construction running on port {port}'); ThreadingHTTPServer(('0.0.0.0', port), App).serve_forever()
