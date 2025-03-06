import requests
import openai

# URL del tuo sito con lo snippet attivo
WORDPRESS_SITE_URL = "https://tarocchidelweb.netsons.org"  # Cambia con il tuo vero dominio!

def fetch_openai_key():
    try:
        url = f"{WORDPRESS_SITE_URL}/wp-json/samanta-ai/v1/get-api-key"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        api_key = data.get("api_key", None)

        if not api_key:
            raise ValueError("Chiave API non trovata o vuota")

        return api_key
    except Exception as e:
        print(f"Errore nel recupero della chiave API: {e}")
        return None

# Carica la chiave OpenAI all'avvio della app
openai.api_key = fetch_openai_key()

if not openai.api_key:
    raise Exception("Impossibile recuperare la chiave OpenAI dal sito WordPress. Controlla lo snippet e il sito!")

