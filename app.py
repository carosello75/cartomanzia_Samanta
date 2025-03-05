from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import os
import tempfile
import openai

app = Flask(__name__)

# Chiave API di OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_cartomante_response(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sei Samanta, una cartomante AI, amichevole e misteriosa."},
                {"role": "user", "content": question}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Errore: {str(e)}"

@app.route('/')
def home():
    return 'Samanta AI è online e pronta per leggere il tuo destino!'

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
    app.run(host='0.0.0.0', port=10000)
