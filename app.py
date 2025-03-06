from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import tempfile
import os
import requests
from openai import OpenAI

# URL del tuo sito WordPress con lo snippet attivo
WORDPRESS_SITE_URL = "https://tarocchidelweb.netsons.org"  # Cambialo col tuo dominio vero

app = Flask(__name__)

# Funzione per recuperare la chiave API da WordPress
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

# Recupera la chiave API all'avvio
openai_api_key = fetch_openai_key()

if not openai_api_key:
    raise Exception("Impossibile recuperare la chiave OpenAI dal sito WordPress. Controlla lo snippet e il sito!")

# Inizializza il client OpenAI con la chiave
client = OpenAI(api_key=openai_api_key)

@app.route('/')
def home():
    return 'Benvenuto! Per parlare con Samanta, usa: /chat?question=Ciao%20Samanta'

@app.route('/chat', methods=['GET'])
def chat():
    question = request.args.get('question', '')
    if not question:
        return jsonify({'errore': 'Nessuna domanda ricevuta'}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sei Samanta, una cartomante virtuale pronta a leggere le carte e rispondere alle domande delle persone."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({'risposta': answer})
    except Exception as e:
        return jsonify({'errore': f'Errore di comunicazione con OpenAI: {str(e)}'}), 500

@app.route('/voice', methods=['GET'])
def voice():
    text = request.args.get('text', '')
    if not text:
        return "Nessun testo fornito", 400

    tts = gTTS(text=text, lang='it')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)

    response = send_file(temp_file.name, mimetype="audio/mpeg")

    @response.call_on_close
    def cleanup():
        os.unlink(temp_file.name)

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

