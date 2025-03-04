import openai
import os
from gtts import gTTS
import base64

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_cartomante_response(user_input):
    client = openai.OpenAI(api_key=openai.api_key)

    messaggi = [
        {"role": "system", "content": "Sei Samanta, una cartomante 
virtuale pronta a leggere le carte e rispondere alle domande delle 
persone."},
        {"role": "user", "content": user_input}
    ]

    risposta = client.chat.completions.create(
        model="gpt-4",
        messages=messaggi,
        max_tokens=200
    )

    return risposta.choices[0].message.content

def generate_voice_response(text):
    tts = gTTS(text=text, lang='it')
    tts.save("response.mp3")

    with open("response.mp3", "rb") as audio_file:
        encoded_audio = 
base64.b64encode(audio_file.read()).decode("utf-8")

    return encoded_audio

