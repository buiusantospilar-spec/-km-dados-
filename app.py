import requests
import os
import time
import random
from flask import Flask, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MOTOR FIXO V7 ULTRA - SINCRONISMO REAL COM A EVOLUTION
# Corrigido com base na estrutura real da API: item['data']['result']['outcome']

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
            raw_data = resp.json()
            normalized = []
            
            for item in raw_data:
                # A estrutura correta é: item['data']['result']
                game_data = item.get('data', {})
                result_obj = game_data.get('result', {})
                outcome = result_obj.get('outcome', '')
                
                # Mapeamento preciso
                res = 'T'
                if outcome == 'PlayerWon': res = 'P'
                elif outcome == 'BankerWon': res = 'B'
                elif outcome == 'Tie': res = 'T'
                else:
                    # Fallback extra pelo placar se o outcome falhar
                    p_score = result_obj.get('playerDice', {}).get('score', 0)
                    b_score = result_obj.get('bankerDice', {}).get('score', 0)
                    if p_score > b_score: res = 'P'
                    elif b_score > p_score: res = 'B'
                    else: res = 'T'

                normalized.append({
                    'result': res,
                    'playerScore': result_obj.get('playerDice', {}).get('score', 0),
                    'bankerScore': result_obj.get('bankerDice', {}).get('score', 0),
                    'id': item.get('id')
                })
            return jsonify(normalized)
        return jsonify([])
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify([])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host="0.0.0.0", port=port)
