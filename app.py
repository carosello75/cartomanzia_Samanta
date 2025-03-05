from flask import Flask, request, send_file
import openai
from gtts import gTTS
import os

app = Flask(__name__)

# Chiave API OpenAI presa dall'ambiente (Render-ready)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return 'Benvenuto! Per parlare con Samanta, usa: 
/chat?question=Ciao%20Samanta'

@app.route('/chat', methods=['GET'])
def chat():
    question = request.args.get('question', '')
    if not question:
        return "Devi fare una domanda!", 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}]
        )
        answer = response['choices'][0]['message']['content']
        return answer
    except Exception as e:
        return f"Errore: {str(e)}", 500

@app.route('/voice', methods=['GET'])
def voice():
    text = request.args.get('text', '')
    if not text:
        return "Nessun testo ricevuto!", 400

    try:
        tts = gTTS(text=text, lang='it')
        tts.save("response.mp3")
        return send_file("response.mp3", mimetype="audio/mpeg")
    except Exception as e:
        return f"Errore nella sintesi vocale: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

