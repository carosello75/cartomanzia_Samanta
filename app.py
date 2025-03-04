from flask import Flask, request, jsonify
from gpt_logic import get_cartomante_response

app = Flask(__name__)

@app.route('/chat', methods=['GET'])
def chat():
    question = request.args.get('question', '')
    if not question:
        return jsonify({'error': 'Domanda mancante'}), 400

    response = get_cartomante_response(question)
    return f"<h2>Risposta di Samanta:</h2><p>{response}</p>"

if __name__ == '__main__':
    app.run(debug=True)
