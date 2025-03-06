from flask import Flask, request, jsonify
from gpt_logic import get_cartomante_response, generate_voice_response
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Benvenuto! Per parlare con Samanta, vai su /chat e aggiungi ?question=la tua domanda'

@app.route('/chat', methods=['GET'])
def chat():
    question = request.args.get('question')
    if not question:
        return jsonify({'error': 'Specifica una domanda nella query string'}), 400

    risposta = get_cartomante_response(question)
    return jsonify({'response': risposta})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render utilizza la variabile PORT
    app.run(host='0.0.0.0', port=port)

