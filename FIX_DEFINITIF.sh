#!/bin/bash
# FIX DÉFINITIF - Configure passenger_wsgi.py pour utiliser les packages --user

cd /home/wrbh3411/fitgang.fr

echo "🔧 Configuration des packages utilisateur..."

# passenger_wsgi.py qui inclut les packages --user
cat > passenger_wsgi.py << 'WSGIEOF'
import sys
import os
import site

# Ajouter les packages installés avec --user
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.insert(0, user_site)

# Ajouter le répertoire courant
sys.path.insert(0, os.path.dirname(__file__))

# Charger .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Créer l'application
from app import create_app
application = create_app('production')
WSGIEOF

# .htaccess simple
cat > .htaccess << 'HTEOF'
PassengerEnabled on
PassengerPython /usr/bin/python3
PassengerAppRoot /home/wrbh3411/fitgang.fr
PassengerStartupFile passenger_wsgi.py
SetEnv FLASK_ENV production
PassengerFriendlyErrorPages off
HTEOF

# Restart
echo "🔄 Redémarrage..."
pkill -9 python 2>/dev/null
rm -rf tmp && mkdir tmp
find . -name "*.pyc" -delete 2>/dev/null
touch passenger_wsgi.py
sleep 15

HTTP=$(curl -k -s -o /dev/null -w "%{http_code}" https://fitgang.fr/ --max-time 10)
echo ""
if [ "$HTTP" = "200" ]; then
    echo "✅ ✅ ✅ SUCCÈS ! ✅ ✅ ✅"
    echo "Site: https://fitgang.fr"
else
    echo "Code HTTP: $HTTP"
    echo "Teste: https://fitgang.fr"
fi
