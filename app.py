from flask import Flask, send_file, jsonify
from flask_cors import CORS
import requests
import os
import time
import random

app = Flask(__name__)
CORS(app)

# Lista de User-Agents para rotacionar e evitar bloqueios
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

API_URL = "https://api-cs.casino.org/svc-evolution-game-events/api/bacbo"

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/bacbo")
def bacbo():
    try:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Origin": "https://www.casino.org",
            "Referer": "https://www.casino.org/",
            "Accept": "application/json",
            "Cache-Control": "no-cache"
        }
        
        # Bypass de Cache e Cloudflare simples com timestamp aleatório
        url = f"{API_URL}?t={int(time.time() * 1000)}&rand={random.randint(1, 1000)}"
        
        # Aumentamos o timeout
        resp = requests.get(url, headers=headers, timeout=20)
        
        if resp.status_code == 403 or resp.status_code == 429:
            print("AVISO: Bloqueio detectado (403/429)")
            return jsonify({"error": "IP Temporariamente Bloqueado"}), 503
            
        data = resp.json()
        
        if isinstance(data, list):
            return jsonify(data)
        elif isinstance(data, dict) and "events" in data:
            return jsonify(data["events"])
        else:
            return jsonify([])
            
    except Exception as e:
        print(f"Erro na conexão com API: {e}")
        return jsonify({"error": "Falha na Rede Original"}), 502

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host="0.0.0.0", port=port)
