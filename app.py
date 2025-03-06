import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Carica le variabili d'ambiente da Render (o .env in locale)
load_dotenv()

# Legge la chiave API da ENV (Render Config Vars o .env in locale)
openai_api_key = os.getenv("OPENAI_API_KEY")

# Controllo se la chiave è presente
if not openai_api_key:
    raise Exception("❌ OPENAI_API_KEY non trovata! Assicurati di averla configurata su Render o in un file .env")

# Inizializza il client OpenAI (senza `proxies`, compatibile con openai>=1.0.0)
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
            messages=[{"role": "system", "content": "Tu sei Samanta, una cartomante virtuale simpatica, intrigante e spiritosa."},
                      {"role": "user", "content": question}]
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({'risposta': reply})

    except Exception as e:
        return jsonify({'errore': f'Errore di comunicazione con OpenAI: {e}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

