from flask import Flask, send_file, jsonify
from flask_cors import CORS
import requests
import os
import time

app = Flask(__name__)
CORS(app)

API_URL = "https://api-cs.casino.org/svc-evolution-game-events/api/bacbo"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Origin": "https://www.casino.org",
    "Referer": "https://www.casino.org/casinoscores/pt-br/bac-bo/",
    "Accept": "application/json",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/bacbo")
def bacbo():
    try:
        url = f"{API_URL}?_={int(time.time() * 1000)}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        
        # LOG PARA DEBUG - Vamos ver o que a API está mandando
        print(f"API Response: {str(data)[:200]}...")
        
        # Garante que sempre retornamos uma lista, mesmo que vazia
        if isinstance(data, list):
            return jsonify(data)
        elif isinstance(data, dict) and "events" in data:
            return jsonify(data["events"])
        else:
            return jsonify([])
            
    except Exception as e:
        print(f"Error fetching API: {e}")
        return jsonify({"error": str(e)}), 502

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host="0.0.0.0", port=port)
