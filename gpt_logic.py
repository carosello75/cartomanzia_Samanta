import os
import requests
from gtts import gTTS
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Carica variabili d'ambiente se esiste un .env locale (utile in sviluppo)
load_dotenv()

# URL del tuo sito WordPress e dell'endpoint che espone la chiave
WORDPRESS_API_URL = "https://tarocchidelweb.netsons.org/wp-json/samanta-ai/v1/get-api-key"

def get_openai_api_key():
    """
    Recupera dinamicamente la chiave OpenAI dal tuo sito WordPress.
    """
    try:
        response = requests.get(WORDPRESS_API_URL)
        response.raise_for_status()
        data = response.json()
        api_key = data.get('api_key', None)
        if not api_key:
            raise ValueError("❌ Chiave API non trovata nell'endpoint WordPress!")
        return api_key
    except Exception as e:
        raise Exception(f"Errore nel recupero chiave da WordPress: {e}")

# Leggi la chiave in tempo reale
api_key = get_openai_api_key()

# Inizializza client OpenAI
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

