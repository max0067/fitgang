#!/bin/bash
# RESET COMPLET V2 - Python 3.6 compatible

set -e

cd /home/wrbh3411

echo "🔥 RESET COMPLET DE FITGANG.FR (Python 3.6)"
echo ""

# 1. SAUVEGARDE BASE DE DONNÉES
echo "1. Sauvegarde de la base de données..."
if [ -f fitgang.fr/fitgang.db ]; then
    cp fitgang.fr/fitgang.db /home/wrbh3411/fitgang_db_backup_$(date +%Y%m%d_%H%M%S).db
    echo "   ✅ Base sauvegardée"
else
    echo "   ⚠️  Aucune base trouvée"
fi

# 2. ARRÊT
echo ""
echo "2. Arrêt processus Python..."
pkill -9 python 2>/dev/null || true
sleep 2

# 3. SUPPRESSION
echo ""
echo "3. Suppression complète..."
cd /home/wrbh3411
rm -rf fitgang.fr
mkdir -p fitgang.fr
cd fitgang.fr

# 4. TÉLÉCHARGEMENT
echo ""
echo "4. Téléchargement depuis GitHub..."
curl -L https://github.com/max0067/fitgang/archive/a848463.tar.gz -o source.tar.gz
tar -xzf source.tar.gz
FOLDER=$(ls -d fitgang-* | head -n 1)
mv $FOLDER/* .
mv $FOLDER/.* . 2>/dev/null || true
rm -rf $FOLDER source.tar.gz
echo "   ✅ Code installé"

# 5. VENV PROPRE POUR PYTHON 3.6
echo ""
echo "5. Création virtualenv Python 3.6..."
python3 -m venv venv --without-pip
curl https://bootstrap.pypa.io/pip/3.6/get-pip.py -o get-pip.py
venv/bin/python get-pip.py > /dev/null 2>&1
rm get-pip.py
echo "   ✅ Venv créé"

# 6. INSTALLATION DÉPENDANCES PYTHON 3.6
echo ""
echo "6. Installation dépendances..."
venv/bin/pip install Flask==2.0.3 > /dev/null 2>&1
venv/bin/pip install Flask-SQLAlchemy==2.5.1 > /dev/null 2>&1
venv/bin/pip install Flask-Login==0.5.0 > /dev/null 2>&1
venv/bin/pip install Flask-WTF==1.0.1 > /dev/null 2>&1
venv/bin/pip install WTForms==3.0.0 > /dev/null 2>&1
venv/bin/pip install Flask-Mail==0.9.1 > /dev/null 2>&1
venv/bin/pip install python-dotenv==0.19.2 > /dev/null 2>&1
venv/bin/pip install Pillow==8.4.0 > /dev/null 2>&1
venv/bin/pip install email-validator==1.1.3 > /dev/null 2>&1
echo "   ✅ Dépendances installées"

# 7. .ENV
echo ""
echo "7. Configuration .env..."
cat > .env << 'ENVEOF'
SECRET_KEY=fitgang-production-secret-key-2024
DATABASE_URL=sqlite:///fitgang.db
FLASK_ENV=production
MAIL_SERVER=mail.fitgang.fr
MAIL_PORT=465
MAIL_USE_SSL=true
MAIL_USERNAME=admin@fitgang.fr
MAIL_DEFAULT_SENDER=admin@fitgang.fr
ADMIN_EMAIL=admin@fitgang.fr
ENVEOF

# 8. BASE DE DONNÉES
echo ""
echo "8. Restauration base de données..."
LATEST_DB=$(ls -t /home/wrbh3411/fitgang_db_backup_*.db 2>/dev/null | head -1)
if [ ! -z "$LATEST_DB" ]; then
    cp "$LATEST_DB" fitgang.db
    echo "   ✅ Base restaurée"
else
    echo "   ⚠️  Aucune base à restaurer"
fi

# 9. PASSENGER_WSGI.PY
echo ""
echo "9. Configuration passenger_wsgi.py..."
cat > passenger_wsgi.py << 'WSGIEOF'
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from app import create_app
application = create_app('production')
WSGIEOF

# 10. .HTACCESS
echo ""
echo "10. Configuration .htaccess..."
cat > .htaccess << 'HTEOF'
PassengerEnabled on
PassengerPython /home/wrbh3411/fitgang.fr/venv/bin/python3
PassengerAppRoot /home/wrbh3411/fitgang.fr
PassengerStartupFile passenger_wsgi.py
SetEnv FLASK_ENV production
PassengerMaxPoolSize 6
PassengerMinInstances 1
HTEOF

# 11. PERMISSIONS
echo ""
echo "11. Permissions..."
chmod 755 /home/wrbh3411/fitgang.fr
chmod 755 app
chmod 644 passenger_wsgi.py .htaccess
chmod 600 .env
chmod 644 fitgang.db 2>/dev/null || true

# 12. TEST
echo ""
echo "12. Test application..."
venv/bin/python << 'PYEOF'
import sys
sys.path.insert(0, '/home/wrbh3411/fitgang.fr')
try:
    from dotenv import load_dotenv
    load_dotenv('/home/wrbh3411/fitgang.fr/.env')
    from app import create_app
    app = create_app('production')
    print("   ✅ Application OK")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)
PYEOF

# 13. DÉMARRAGE
echo ""
echo "13. Démarrage Passenger..."
mkdir -p tmp
touch passenger_wsgi.py
echo "$(date)" > tmp/restart.txt
sleep 30

# 14. TEST FINAL
echo ""
echo "14. Test final..."
HTTP=$(curl -k -s -o /dev/null -w "%{http_code}" https://fitgang.fr/ --max-time 15)

echo ""
echo "=== RÉSULTAT ==="
echo "Code HTTP: $HTTP"
echo ""

if [ "$HTTP" = "200" ]; then
    echo "✅ ✅ ✅ SUCCÈS ! ✅ ✅ ✅"
    echo ""
    echo "🎉 https://fitgang.fr"
    echo "🎉 https://fitgang.fr/dashboard"
    echo ""
else
    echo "⚠️  Code: $HTTP"
    echo ""
    echo "Vérifie: https://fitgang.fr"
fi

echo ""
echo "=== TERMINÉ ==="
