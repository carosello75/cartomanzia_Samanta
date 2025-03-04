from flask import Flask, request, jsonify
from gpt_logic import get_cartomante_response

app = Flask(__name__)

@app.route('/chat', methods=['GET'])
def chat():
    question = request.args.get('question', '')
    if not question:
        return jsonify({'error': 'Domanda mancante'}), 400

    response = get_cartomante_response(question)
    return jsonify({'risposta': response})

@app.route('/')
def home():
    return "Benvenuto! Per parlare con Samanta, usa: 
/chat?question=Ciao%20Samanta"

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)

