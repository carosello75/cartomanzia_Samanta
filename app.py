import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Carica le variabili d'ambiente da Render (o da un file .env in locale)
load_dotenv()

# Legge la chiave API da ENV
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise Exception("❌ OPENAI_API_KEY non trovata! Assicurati di averla configurata su Render o in un file .env")

# Imposta la chiave API per il modulo openai
openai.api_key = openai_api_key

# Inizializza Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Benvenuto! Per parlare con Samanta, usa: /chat?question=Ciao%20Samanta'

@app.route('/chat', methods=['GET'])
def chat():
    question = request.args.get('question', '')
    if not question:
        return jsonify({'errore': 'Domanda mancante! Passa la domanda come query param: ?question=...'})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu sei Samanta, una cartomante virtuale simpatica, intrigante e spiritosa."},
                {"role": "user", "content": question}
            ]
        )
        return jsonify(response)
    except Exception as e:
        return jsonify({'errore': f"Errore di comunicazione con OpenAI: {str(e)}"})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

