from flask import Flask, request, jsonify, send_file
from gpt_logic import get_cartomante_response, generate_voice_response

app = Flask(__name__)

@app.route('/')
def home():
    return 'Benvenuto! Samanta è online e pronta a rispondere.'

@app.route('/chat', methods=['GET'])
def chat():
    question = request.args.get('question')
    if not question:
        return jsonify({'errore': 'Nessuna domanda fornita'}), 400

    risposta = get_cartomante_response(question)
    return jsonify({'risposta': risposta})

@app.route('/voice', methods=['GET'])
def voice():
    text = request.args.get('text')
    if not text:
        return jsonify({'errore': 'Nessun testo fornito'}), 400

    file_path = generate_voice_response(text)
    return send_file(file_path, mimetype="audio/mpeg")

