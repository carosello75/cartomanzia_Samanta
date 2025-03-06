#!/bin/bash

echo "✅ Avvio setup ambiente virtuale e installazione pacchetti..."

# Crea venv
python3 -m venv venv

# Attiva venv
source venv/bin/activate

# Installa i pacchetti
pip install -r requirements.txt

# Fine
echo "✅ Setup completato! Ora puoi eseguire: source venv/bin/activate && python app.py"

