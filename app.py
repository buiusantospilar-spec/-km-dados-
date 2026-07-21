from flask import Flask, send_file, jsonify
from flask_cors import CORS
import requests
import os
import time
import random

app = Flask(__name__)
CORS(app)

# URLs alternativas caso a principal falhe
API_URLS = [
    "https://api-cs.casino.org/svc-evolution-game-events/api/bacbo",
    "https://www.casino.org/casinoscores/api/evolution/bacbo" # Possível rota alternativa
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1"
]

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/bacbo")
def bacbo():
    # Tentamos as URLs conhecidas
    for url_base in API_URLS:
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "Referer": "https://www.casino.org/casinoscores/pt-br/bac-bo/",
                "Origin": "https://www.casino.org",
                "Cache-Control": "no-cache",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site"
            }
            
            # Timestamp mais agressivo para evitar cache do Cloudflare
            full_url = f"{url_base}?_t={int(time.time() * 1000)}&v={random.random()}"
            
            # Usando uma sessão para manter cookies básicos se necessário
            session = requests.Session()
            resp = session.get(full_url, headers=headers, timeout=15)
            
            if resp.status_code == 200:
                data = resp.json()
                # Se a API retornar um erro interno mascarado de 200
                if isinstance(data, dict) and data.get('error'):
                    continue
                return jsonify(data)
            
            print(f"Tentativa falhou para {url_base}: Status {resp.status_code}")
            
        except Exception as e:
            print(f"Erro na tentativa com {url_base}: {e}")
            continue
            
    # Se todas as tentativas falharem
    return jsonify({"error": "IP do Render bloqueado pelo fornecedor original. Tente novamente em alguns minutos."}), 503

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host="0.0.0.0", port=port)
