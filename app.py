from flask import Flask, request, jsonify, send_file
from gpt_logic import get_cartomante_response
from gtts import gTTS
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Benvenuto! Per parlare con Samanta, usa: /chat?question=Ciao%20Samanta'

@app.route('/chat', methods=['GET'])
def chat():
    question = request.args.get('question', '')
    if not question:
        return jsonify({'errore': 'Nessuna domanda ricevuta'}), 400

    risposta = get_cartomante_response(question)
    return jsonify({'risposta': risposta})

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

