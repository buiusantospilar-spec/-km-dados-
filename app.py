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
        
        # Bypass de cache com timestamp
        params = {"t": int(time.time() * 1000)}
        
        resp = requests.get(API_URL, headers=headers, params=params, timeout=15)
        
        if resp.status_code == 200:
            raw_data = resp.json()
            
            # Normalização para a V7: Garante que o index.html receba 'result' como P, B ou T
            normalized_data = []
            
            # Se for uma lista direta (comum na API da Evolution)
            items = raw_data if isinstance(raw_data, list) else raw_data.get("events", [])
            
            for item in items:
                # Extração segura da estrutura aninhada da Evolution
                data = item.get('data', {})
                result_obj = data.get('result', {})
                outcome = str(result_obj.get('outcome', '')).strip()
                
                # Extração de dados para análise de soma e placar
                p_dice_obj = result_obj.get('playerDice', {})
                b_dice_obj = result_obj.get('bankerDice', {})
                
                p_score = p_dice_obj.get('score', 0)
                b_score = b_dice_obj.get('score', 0)
                
                res = 'T'
                if outcome == 'PlayerWon': res = 'P'
                elif outcome == 'BankerWon': res = 'B'
                elif outcome == 'Tie' or outcome == 'TieWon': res = 'T'
                
                # Fallback para caso o outcome venha diferente mas o placar seja igual
                if p_score == b_score and p_score > 0:
                    res = 'T'
                
                p_d1 = p_dice_obj.get('first', 0)
                p_d2 = p_dice_obj.get('second', 0)
                b_d1 = b_dice_obj.get('first', 0)
                b_d2 = b_dice_obj.get('second', 0)
                
                new_item = {
                    'result': res,
                    'playerScore': p_score,
                    'bankerScore': b_score,
                    'playerDice': [p_d1, p_d2],
                    'bankerDice': [b_d1, b_d2],
                    'time': time.strftime('%H:%M:%S')
                }
                normalized_data.append(new_item)
            
            return jsonify(normalized_data)
            
        return jsonify([])
        
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify([])

if __name__ == "__main__":
    # Mantém a porta 8888 ou usa a do ambiente
    port = int(os.environ.get("PORT", 8888))
    app.run(host="0.0.0.0", port=port)
