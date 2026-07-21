from flask import Flask, send_file, jsonify
from flask_cors import CORS
import requests
import os
import time
import random

app = Flask(__name__)
CORS(app)

USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

# URL da API direto da Evolution
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
        
        # timestamp para evitar cache do Railway
        params = {"_t": int(time.time() * 1000)}
        
        resp = requests.get(API_URL, headers=headers, params=params, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                # Limpa os dados para garantir que o front-end receba apenas o necessário
                clean_data = []
                for entry in data:
                    res = entry.get('result') or entry.get('type') or entry.get('winner') or 'T'
                    clean_data.append({'result': res})
                return jsonify(clean_data)
            
        return jsonify([])
            
    except Exception as e:
        return jsonify([])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
