import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_cartomante_response(question):
    prompt = f"""
    Tu sei Samanta, una cartomante spiritosa, sensuale e molto sveglia.
    Rispondi come una vera cartomante esperta, con un tocco di malizia e divertimento.
    La tua risposta deve essere coinvolgente e sempre mistica, con frasi intriganti.

    Cliente: {question}
    Samanta:
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu sei Samanta, la cartomante AI, mistica e sensuale."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content.strip()
