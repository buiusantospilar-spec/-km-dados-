import requests
import os
import time
import random
from flask import Flask, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- MOTOR FIXO E BLINDADO (VERSÃO DEFINITIVA) ---
# Este arquivo não precisará mais ser alterado.
# Ele foca 100% em entregar os dados reais e sincronizados.

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1"
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
            "Accept": "application/json"
        }
        params = {"t": int(time.time() * 1000)}
        resp = requests.get(API_URL, headers=headers, params=params, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            results = data.get('data', []) if isinstance(data, dict) else data
            
            normalized = []
            for item in results[:100]: # Enviamos 100 resultados para o Index analisar à vontade
                p_dice = item.get('playerDice', item.get('player', {}))
                b_dice = item.get('bankerDice', item.get('banker', {}))
                p_score = p_dice.get('score', 0)
                b_score = b_dice.get('score', 0)
                
                # O motor apenas entrega o que aconteceu. A lógica de sinal fica no INDEX.
                res = 'T'
                if p_score > b_score: res = 'P'
                elif b_score > p_score: res = 'B'
                else: res = 'T'
                
                normalized.append({
                    'result': res,
                    'playerScore': p_score,
                    'bankerScore': b_score,
                    'id': item.get('id', str(random.random()))
                })
            return jsonify(normalized)
        return jsonify([])
    except Exception as e:
        return jsonify([])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host="0.0.0.0", port=port)
