import os
from gtts import gTTS
import base64
from dotenv import load_dotenv
from openai import OpenAI

# Carica variabili ambiente
load_dotenv()

# Leggi API Key da ENV
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY non trovata! Controlla le variabili d'ambiente.")

# Crea client OpenAI
client = OpenAI(api_key=api_key)

def get_cartomante_response(user_input):
    messaggi = [
        {"role": "system", "content": "Sei Samanta, una cartomante virtuale pronta a leggere le carte e rispondere alle domande delle persone."},
        {"role": "user", "content": user_input}
    ]

    try:
        risposta = client.chat.completions.create(
            model="gpt-4",
            messages=messaggi,
            max_tokens=200
        )
        return risposta.choices[0].message.content
    except Exception as e:
        return f"Errore nella comunicazione con OpenAI: {str(e)}"

def generate_voice_response(text):
    tts = gTTS(text=text, lang='it')
    tts.save("response.mp3")
    
    with open("response.mp3", "rb") as audio_file:
        encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")

    return encoded_audio

