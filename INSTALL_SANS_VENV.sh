#!/bin/bash
# INSTALLATION SANS VENV - Utilise pip --user

set -e

cd /home/wrbh3411/fitgang.fr

echo "🏋️ INSTALLATION COMPLÈTE FITGANG.FR (sans venv)"
echo ""

# 1. BACKUP
echo "1. Backup base de données..."
cp fitgang.db fitgang.db.backup_$(date +%Y%m%d_%H%M%S) 2>/dev/null || true

# 2. NETTOYAGE
echo ""
echo "2. Nettoyage..."
pkill -9 python 2>/dev/null || true
rm -rf app config.py passenger_wsgi.py .htaccess 2>/dev/null || true
rm -rf tmp __pycache__ 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
rm -rf fitgang-* *.tar.gz 2>/dev/null || true

# 3. TÉLÉCHARGEMENT
echo ""
echo "3. Téléchargement version stable..."
curl -L https://github.com/max0067/fitgang/archive/6f5adc1acffb6b682f8948331e9df6f3ffc3cbf2.tar.gz -o stable.tar.gz
tar -xzf stable.tar.gz
FOLDER=$(ls -d fitgang-* | head -n 1)

# 4. INSTALLATION FICHIERS
echo ""
echo "4. Installation fichiers..."
cp -r "$FOLDER/app" .
cp "$FOLDER/config.py" .
rm -rf "$FOLDER" stable.tar.gz

# 5. INSTALLATION DÉPENDANCES
echo ""
echo "5. Installation dépendances Python..."
pip3 install --user Flask==2.0.3 > /dev/null 2>&1
pip3 install --user Flask-SQLAlchemy==2.5.1 > /dev/null 2>&1
pip3 install --user Flask-Login==0.5.0 > /dev/null 2>&1
pip3 install --user Flask-WTF==1.0.1 > /dev/null 2>&1
pip3 install --user WTForms==3.0.0 > /dev/null 2>&1
pip3 install --user Flask-Mail==0.9.1 > /dev/null 2>&1
pip3 install --user python-dotenv==0.19.2 > /dev/null 2>&1
pip3 install --user Pillow==8.4.0 > /dev/null 2>&1
pip3 install --user email-validator==1.1.3 > /dev/null 2>&1
echo "   ✅ Dépendances installées"

# 6. .ENV
echo ""
echo "6. Configuration .env..."
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

# 7. PASSENGER_WSGI.PY (SANS VENV)
echo ""
echo "7. Configuration passenger_wsgi.py..."
cat > passenger_wsgi.py << 'WSGIEOF'
import sys
import os
import site

# Ajouter les packages --user
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.insert(0, user_site)

# Ajouter répertoire courant
sys.path.insert(0, os.path.dirname(__file__))

# Charger .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Créer application
from app import create_app
application = create_app('production')
WSGIEOF

# 8. .HTACCESS
echo ""
echo "8. Configuration .htaccess..."
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

# 9. TEST IMPORT
echo ""
echo "9. Test de l'application..."
python3 -c "from dotenv import load_dotenv; load_dotenv('.env'); from app import create_app; app = create_app('production'); print('✅ Application OK')"

# 10. REDÉMARRAGE
echo ""
echo "10. Redémarrage Passenger..."
mkdir -p tmp
touch passenger_wsgi.py
echo "$(date)" > tmp/restart.txt
pkill -9 python 2>/dev/null || true

echo ""
echo "11. Attente 30 secondes..."
sleep 30

# 11. TEST FINAL
echo ""
echo "12. Test final..."
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
    echo "🎉 https://fitgang.fr/programmes"
    echo ""
else
    echo "⚠️  Code: $HTTP"
    echo ""
    echo "Vérifie: https://fitgang.fr"
fi

echo ""
echo "=== FICHIERS ==="
ls -lh app/ config.py passenger_wsgi.py .env .htaccess fitgang.db 2>/dev/null | head -10

echo ""
echo "=== TERMINÉ ==="
