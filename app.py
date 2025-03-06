import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

# Carica le variabili d'ambiente (Render o .env)
load_dotenv()

# Leggi la chiave API
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise Exception("❌ OPENAI_API_KEY non trovata! Assicurati di averla configurata su Render o nel file .env")

# Inizializza il client OpenAI
client = OpenAI(api_key=openai_api_key)

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
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu sei Samanta, una cartomante virtuale simpatica, intrigante e spiritosa."},
                {"role": "user", "content": question}
            ]
        )

        risposta = response.choices[0].message.content
        return jsonify({'risposta': risposta})

    except Exception as e:
        return jsonify({'errore': f'Errore di comunicazione con OpenAI: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

