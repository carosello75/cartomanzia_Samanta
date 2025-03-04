import openai
import os

def get_cartomante_response(question):
    # Legge la chiave API da variabile d'ambiente
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("La variabile di ambiente OPENAI_API_KEY è 
mancante!")

    # Inizializza il client con la chiave corretta
    client = openai.OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu sei Samanta, una cartomante 
sensuale e spiritosa. Rispondi in modo intrigante e coinvolgente."},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content.strip()

