#!/bin/bash
# FIX FINAL - Change .htaccess pour utiliser Python système qui MARCHE

cd /home/wrbh3411/fitgang.fr

echo "🔧 Configuration finale..."

# .htaccess avec Python SYSTÈME (pas venv)
cat > .htaccess << 'HTEOF'
PassengerEnabled on
PassengerPython /usr/bin/python3
PassengerAppRoot /home/wrbh3411/fitgang.fr
PassengerStartupFile passenger_wsgi.py
SetEnv FLASK_ENV production
PassengerFriendlyErrorPages off
PassengerMaxPoolSize 6
PassengerMinInstances 1
HTEOF

# passenger_wsgi.py simple
cat > passenger_wsgi.py << 'WSGIEOF'
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
from app import create_app
application = create_app('production')
WSGIEOF

# Restart BRUTAL
pkill -9 python 2>/dev/null
rm -rf tmp && mkdir tmp
touch passenger_wsgi.py
find . -name "*.pyc" -delete 2>/dev/null

echo "✅ FAIT - Attente 15 secondes..."
sleep 15

HTTP=$(curl -k -s -o /dev/null -w "%{http_code}" https://fitgang.fr/ --max-time 10)

if [ "$HTTP" = "200" ]; then
    echo ""
    echo "✅ ✅ ✅ SITE EN LIGNE ! ✅ ✅ ✅"
    echo "https://fitgang.fr"
else
    echo ""
    echo "Code: $HTTP - Vérifie https://fitgang.fr"
fi
