#!/bin/bash
# FIX .HTACCESS COMPLET avec PassengerPython

cd /home/wrbh3411/fitgang.fr

echo "🔧 Configuration .htaccess COMPLÈTE..."

# .htaccess avec PassengerPython pointant vers python3 système
cat > .htaccess << 'HTEOF'
PassengerEnabled on
PassengerPython /usr/bin/python3
PassengerAppRoot /home/wrbh3411/fitgang.fr
PassengerStartupFile passenger_wsgi.py
SetEnv FLASK_ENV production
HTEOF

# passenger_wsgi.py qui charge les packages --user
cat > passenger_wsgi.py << 'WSGIEOF'
import sys
import os
import site

# Charger les packages --user
user_site = site.getusersitepackages()
if user_site and user_site not in sys.path:
    sys.path.insert(0, user_site)

# Ajouter le répertoire
sys.path.insert(0, '/home/wrbh3411/fitgang.fr')

# Charger .env
from dotenv import load_dotenv
load_dotenv('/home/wrbh3411/fitgang.fr/.env')

# Créer app
from app import create_app
application = create_app('production')
WSGIEOF

echo "✅ Fichiers configurés"
echo ""
echo "Redémarrage..."

# Redémarrage
pkill -9 python 2>/dev/null
touch passenger_wsgi.py
touch .htaccess
mkdir -p tmp
echo "$(date)" > tmp/restart.txt

sleep 15

HTTP=$(curl -k -s -o /dev/null -w "%{http_code}" https://fitgang.fr/ --max-time 10)

echo ""
echo "=== RÉSULTAT ==="
echo "Code: $HTTP"
echo ""

if [ "$HTTP" = "200" ]; then
    echo "✅ ✅ ✅ SUCCÈS ! ✅ ✅ ✅"
    echo ""
    echo "https://fitgang.fr"
else
    echo "⚠️  Toujours $HTTP"
    echo ""
    echo "Il faut restaurer depuis un backup qui marchait."
    echo "Contacte le support o2switch pour restaurer"
    echo "une version du site qui fonctionnait."
fi
