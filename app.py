from flask import Flask, send_file, jsonify
from flask_cors import CORS
import requests
import os
import time
import random

app = Flask(__name__)
CORS(app)

# Lista de User-Agents para rotacionar
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
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
            "Accept": "application/json",
            "Referer": "https://www.casino.org/",
            "Origin": "https://www.casino.org"
        }
        
        # Força bypass de cache
        url = f"{API_URL}?t={int(time.time() * 1000)}"
        
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            # Log para ver se os dados estão chegando no console do Railway
            print(f"Dados recebidos: {len(data) if isinstance(data, list) else 'Erro no formato'}")
            return jsonify(data if isinstance(data, list) else [])
            
        print(f"Erro na API Original: Status {resp.status_code}")
        return jsonify({"error": "API Offline"}), 503
            
    except Exception as e:
        print(f"Erro no Proxy: {e}")
        return jsonify({"error": str(e)}), 502

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080)) # Porta padrão Railway
    app.run(host="0.0.0.0", port=port)
