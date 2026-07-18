#!/usr/bin/env python3
"""
Km Dados – Servidor local para o app Bac Bo ao Vivo
Execute: python3 server.py
Acesse:  http://localhost:8888
"""

import json
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

API_URL = "https://api-cs.casino.org/svc-evolution-game-events/api/bacbo"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Origin": "https://www.casino.org",
    "Referer": "https://www.casino.org/casinoscores/pt-br/bac-bo/",
    "Accept": "application/json",
}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # silenciar logs do servidor

    def send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            # Servir o HTML principal
            html_path = os.path.join(os.path.dirname(__file__), "index.html")
            with open(html_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_cors()
            self.end_headers()
            self.wfile.write(content)

        elif self.path == "/api/bacbo":
            # Proxy para a API do casino
            try:
                req = urllib.request.Request(API_URL, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = resp.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors()
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_response(502)
                self.send_header("Content-Type", "application/json")
                self.send_cors()
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    PORT = 8888
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"""
╔══════════════════════════════════════╗
║     🎲  Km Dados – Bac Bo ao Vivo   ║
╚══════════════════════════════════════╝

  ✅ Servidor rodando!
  👉 Abra no navegador: http://localhost:{PORT}

  (Pressione Ctrl+C para parar)
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor encerrado.")
