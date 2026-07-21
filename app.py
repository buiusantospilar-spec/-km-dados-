import requests
import os
import time
import random
from flask import Flask, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MOTOR ORIGINAL E ESTÁVEL - O QUE VOCÊ MANDOU
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
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
            "Accept": "application/json"
        }
        params = {"t": int(time.time() * 1000)}
        resp = requests.get(API_URL, headers=headers, params=params, timeout=10)
        
        if resp.status_code == 200:
            # Entrega os dados puros para o index processar
            return jsonify(resp.json())
        return jsonify([])
    except Exception as e:
        print(f"Erro na API: {e}")
        return jsonify([])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host="0.0.0.0", port=port)
