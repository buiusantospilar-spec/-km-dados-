import requests
import os
import time
import random
from flask import Flask, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MOTOR ORIGINAL - ESTÁVEL E SIMPLES
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

# API direta da Casino.org que sempre funcionou bem no início
API_URL = "https://api-cs.casino.org/svc-evolution-game-events/api/bacbo"

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/bacbo")
def bacbo():
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        params = {"t": int(time.time() * 1000)}
        resp = requests.get(API_URL, headers=headers, params=params, timeout=10)
        
        if resp.status_code == 200:
            # Retorna o JSON puro para o index processar, como era no começo
            return jsonify(resp.json())
        return jsonify([])
    except Exception:
        return jsonify([])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host="0.0.0.0", port=port)
