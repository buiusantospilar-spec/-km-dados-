from flask import Flask, send_file, jsonify
from flask_cors import CORS
import requests
import os
import time
import random

app = Flask(__name__)
CORS(app)

# Lista de User-Agents mobile para simular iPhone
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
]

# URL da API direto da Evolution (via proxy do Casino.org para evitar block)
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
            "Referer": "https://www.casino.org/online-casinos/free-games/bac-bo/",
            "Origin": "https://www.casino.org"
        }
        
        # timestamp para evitar cache do Railway
        params = {"_t": int(time.time() * 1000)}
        
        resp = requests.get(API_URL, headers=headers, params=params, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                # Retorna os dados reais da mesa
                return jsonify(data)
            
        return jsonify({"error": "Formato de dados invalido"}), 500
            
    except Exception as e:
        print(f"Erro no Proxy: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
