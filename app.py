from flask import Flask, request, jsonify
import requests
import openai
import os
from dotenv import load_dotenv

# Carichiamo il file .env se esiste (per sicurezza)
load_dotenv()

# URL del tuo sito con lo snippet attivo
WORDPRESS_SITE_URL = "https://tarocchidelweb.netsons.org"  # cambia con il tuo dominio corretto

def fetch_openai_key():
    try:
        url = f"{WORDPRESS_SITE_URL}/wp-json/samanta-ai/v1/get-api-key"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        api_key = data.get("api_key", None)

        if not api_key:
            raise ValueError("Chiave API non trovata o vuota")

        return api_key
    except Exception as e:
        print(f"Errore nel recupero della chiave API: {e}")
        return None

# Recuperiamo la chiave OpenAI e la configuriamo
openai.api_key = fetch_openai_key()

if not openai.api_key:
    raise Exception("Impossibile recuperare la chiave OpenAI dal sito WordPress. Controlla lo snippet e il sito!")

app = Flask(__name__)

@app.route("/")
def home():
    return 'Benvenuto! Per parlare con Samanta, usa: /chat?question=Ciao%20Samanta'

@app.route("/chat", methods=["GET"])
def chat():
    question = request.args.get("question", "")

    if not question:
        return jsonify({"errore": "Devi fornire una domanda usando il parametro 'question'."})

    try:
        # Chiamata OpenAI aggiornata (nuovo metodo 1.x)
        response = openai.chat.completions.create(
            model="gpt-4",  # puoi cambiare in gpt-4 o altro se serve
            messages=[
                {"role": "system", "content": "Tu sei Samanta, una cartomante simpatica, spiritosa e intrigante."},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=500
        )

        reply = response.choices[0].message.content.strip()

        return jsonify({"risposta": reply})

    except Exception as e:
        return jsonify({"errore": f"Errore di comunicazione con OpenAI: {e}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

