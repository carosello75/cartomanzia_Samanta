import openai
import os

def get_cartomante_response(question):
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei Samanta, una cartomante 
simpatica e sensuale che risponde con tono divertente, intrigante e un po' 
malizioso."},
            {"role": "user", "content": question}
        ]
    )

    return response['choices'][0]['message']['content']

