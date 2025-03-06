from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from gpt_logic import get_cartomante_response, generate_voice_response

app = Flask(__name__)
CORS(app)  # Abilita CORS

@app.route('/')
def home():
    return "API di Samanta è attiva!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Messaggio non fornito"}), 400

    try:
        risposta = get_cartomante_response(user_message)
        audio_base64 = generate_voice_response(risposta)
        return jsonify({"risposta": risposta, "audio": audio_base64})

    except Exception as e:
        return jsonify({"error": f"Errore interno: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Questo prende la porta da Render
    app.run(host="0.0.0.0", port=port)

