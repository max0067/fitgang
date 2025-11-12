#!/bin/bash
# FIX PERMISSIONS ET CONFIGURATION BASIQUE

cd /home/wrbh3411/fitgang.fr

echo "🔧 Vérification et correction des permissions..."

# 1. Permissions correctes
echo ""
echo "1. Correction des permissions..."
chmod 755 . 2>/dev/null
chmod 644 passenger_wsgi.py 2>/dev/null
chmod 644 .htaccess 2>/dev/null
chmod 644 config.py 2>/dev/null
chmod 644 .env 2>/dev/null
chmod 755 app 2>/dev/null
chmod 644 app/*.py 2>/dev/null
chmod 755 app/static 2>/dev/null
chmod 755 app/templates 2>/dev/null

# 2. .htaccess ULTRA BASIQUE
echo ""
echo "2. Configuration .htaccess basique..."
cat > .htaccess << 'HTEOF'
PassengerEnabled on
PassengerAppRoot /home/wrbh3411/fitgang.fr
HTEOF

# 3. passenger_wsgi.py ULTRA SIMPLE
echo ""
echo "3. passenger_wsgi.py ultra-simple..."
cat > passenger_wsgi.py << 'WSGIEOF'
import sys, os

# Ajouter le répertoire
sys.path.insert(0, '/home/wrbh3411/fitgang.fr')

# Charger dotenv
try:
    from dotenv import load_dotenv
    load_dotenv('/home/wrbh3411/fitgang.fr/.env')
except:
    pass

# Importer l'app
from app import create_app
application = create_app('production')
WSGIEOF

# 4. Vérifications
echo ""
echo "4. Vérifications..."
echo -n "   app/ existe: "
[ -d app ] && echo "✅" || echo "❌"

echo -n "   config.py existe: "
[ -f config.py ] && echo "✅" || echo "❌"

echo -n "   .env existe: "
[ -f .env ] && echo "✅" || echo "❌"

echo -n "   fitgang.db existe: "
[ -f fitgang.db ] && echo "✅" || echo "❌"

# 5. Test import Python
echo ""
echo "5. Test import..."
python3 << 'PYEOF'
import sys
sys.path.insert(0, '/home/wrbh3411/fitgang.fr')
try:
    from dotenv import load_dotenv
    load_dotenv('/home/wrbh3411/fitgang.fr/.env')
    from app import create_app
    app = create_app('production')
    print("   ✅ Import OK")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
PYEOF

# 6. Redémarrage BRUTAL
echo ""
echo "6. Redémarrage..."
pkill -9 python 2>/dev/null
rm -rf tmp 2>/dev/null
mkdir -p tmp
touch passenger_wsgi.py
touch .htaccess
echo "$(date)" > tmp/restart.txt

# Attendre
echo ""
echo "7. Attente 20 secondes..."
sleep 20

# Test
HTTP=$(curl -k -s -o /dev/null -w "%{http_code}" https://fitgang.fr/ --max-time 10 2>/dev/null)

echo ""
echo "=== RÉSULTAT ==="
echo "Code HTTP: $HTTP"
echo ""

if [ "$HTTP" = "200" ]; then
    echo "✅ ✅ ✅ ÇA MARCHE ! ✅ ✅ ✅"
    echo ""
    echo "https://fitgang.fr"
else
    echo "⚠️  Toujours code $HTTP"
    echo ""
    echo "Prochaine étape: contacter le support o2switch"
    echo "Il y a peut-être un problème de configuration Passenger"
    echo "au niveau serveur."
fi

echo ""
echo "=== TERMINÉ ==="
