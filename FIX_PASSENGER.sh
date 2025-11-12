#!/bin/bash
# FIX PASSENGER_WSGI.PY - Version ultra-simple qui MARCHE

cd /home/wrbh3411/fitgang.fr

echo "🔧 Correction de passenger_wsgi.py..."

# Créer un passenger_wsgi.py SIMPLE qui marche
cat > passenger_wsgi.py << 'WSGIEOF'
import sys
import os

# Ajouter le répertoire courant au path
INTERP = "/home/wrbh3411/.local/bin/python3"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.dirname(__file__))

# Charger les variables d'environnement depuis .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Importer l'application Flask
from app import create_app
application = create_app('production')
WSGIEOF

echo "✅ passenger_wsgi.py corrigé"

# Redémarrage brutal
echo ""
echo "🔄 Redémarrage..."
pkill -9 python 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null
rm -rf tmp && mkdir tmp
touch passenger_wsgi.py
echo "$(date)" > tmp/restart.txt

sleep 10

echo ""
echo "✅ TERMINÉ"
echo ""
echo "Teste maintenant: https://fitgang.fr"
WSGIEOF

chmod +x FIX_PASSENGER.sh

echo ""
echo "✅ Script créé"
echo ""
echo "Exécute sur le serveur:"
echo "  bash FIX_PASSENGER.sh"
