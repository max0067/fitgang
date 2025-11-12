#!/bin/bash
# RÉINSTALLATION COMPLÈTE DE A à Z
# Tout nettoyer et réinstaller proprement

set -e

cd /home/wrbh3411/fitgang.fr

echo "🏋️ RÉINSTALLATION COMPLÈTE DE FITGANG.FR"
echo ""

# 1. BACKUP de la base de données
echo "1. Backup de la base de données..."
cp fitgang.db fitgang.db.backup_$(date +%Y%m%d_%H%M%S) 2>/dev/null || true

# 2. NETTOYAGE COMPLET
echo ""
echo "2. Nettoyage complet..."
pkill -9 python 2>/dev/null || true
rm -rf app config.py passenger_wsgi.py 2>/dev/null || true
rm -rf venv 2>/dev/null || true
rm -rf tmp __pycache__ 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
rm -rf fitgang-* 2>/dev/null || true

# 3. TÉLÉCHARGEMENT VERSION STABLE
echo ""
echo "3. Téléchargement version stable (6f5adc1)..."
curl -L https://github.com/max0067/fitgang/archive/6f5adc1acffb6b682f8948331e9df6f3ffc3cbf2.tar.gz -o stable.tar.gz
tar -xzf stable.tar.gz
FOLDER=$(ls -d fitgang-* | head -n 1)

# 4. COPIE DES FICHIERS
echo ""
echo "4. Installation des fichiers..."
cp -r "$FOLDER/app" .
cp "$FOLDER/config.py" .
cp "$FOLDER/requirements.txt" . 2>/dev/null || true
rm -rf "$FOLDER" stable.tar.gz

# 5. CRÉATION VENV PROPRE
echo ""
echo "5. Création virtualenv propre..."
python3 -m venv venv
source venv/bin/activate

# 6. INSTALLATION DÉPENDANCES
echo ""
echo "6. Installation des dépendances..."
pip install --upgrade pip > /dev/null 2>&1
pip install Flask==2.0.3 > /dev/null 2>&1
pip install Flask-SQLAlchemy==2.5.1 > /dev/null 2>&1
pip install Flask-Login==0.5.0 > /dev/null 2>&1
pip install Flask-WTF==1.0.1 > /dev/null 2>&1
pip install WTForms==3.0.0 > /dev/null 2>&1
pip install Flask-Mail==0.9.1 > /dev/null 2>&1
pip install python-dotenv==0.19.2 > /dev/null 2>&1
pip install Pillow==8.4.0 > /dev/null 2>&1
pip install email-validator==1.1.3 > /dev/null 2>&1
echo "   ✅ Dépendances installées"

deactivate

# 7. CONFIGURATION .ENV
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

# 8. PASSENGER_WSGI.PY
echo ""
echo "8. Configuration passenger_wsgi.py..."
cat > passenger_wsgi.py << 'WSGIEOF'
import sys
import os

INTERP = os.path.join(os.path.dirname(__file__), 'venv', 'bin', 'python3')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from app import create_app
application = create_app('production')
WSGIEOF

# 9. .HTACCESS
echo ""
echo "9. Configuration .htaccess..."
cat > .htaccess << 'HTEOF'
PassengerEnabled on
PassengerPython /home/wrbh3411/fitgang.fr/venv/bin/python3
PassengerAppRoot /home/wrbh3411/fitgang.fr
PassengerStartupFile passenger_wsgi.py
SetEnv FLASK_ENV production
PassengerFriendlyErrorPages off
PassengerMaxPoolSize 6
PassengerMinInstances 1
HTEOF

# 10. VÉRIFICATION BASE DE DONNÉES
echo ""
echo "10. Vérification base de données..."
if [ -f fitgang.db ]; then
    echo "    ✅ Base de données existe"
else
    echo "    ⚠️  Base de données manquante"
fi

# 11. REDÉMARRAGE
echo ""
echo "11. Redémarrage Passenger..."
mkdir -p tmp
touch passenger_wsgi.py
echo "$(date)" > tmp/restart.txt
pkill -9 python 2>/dev/null || true

echo ""
echo "12. Attente 30 secondes..."
sleep 30

# 12. TEST FINAL
echo ""
echo "13. Test final..."
HTTP=$(curl -k -s -o /dev/null -w "%{http_code}" https://fitgang.fr/ --max-time 15)

echo ""
echo "=== RÉSULTAT FINAL ==="
echo "Code HTTP: $HTTP"
echo ""

if [ "$HTTP" = "200" ]; then
    echo "✅ ✅ ✅ SUCCÈS TOTAL ! ✅ ✅ ✅"
    echo ""
    echo "🎉 Site EN LIGNE: https://fitgang.fr"
    echo "🎉 Dashboard: https://fitgang.fr/dashboard"
    echo ""
else
    echo "⚠️  Le site retourne le code $HTTP"
    echo ""
    echo "Diagnostics:"
    echo "  - Test manuel: https://fitgang.fr"
    echo "  - Venv Python: $(venv/bin/python3 --version)"
    echo "  - Test import: venv/bin/python3 -c 'from app import create_app; print(\"OK\")'"
fi

echo ""
echo "=== STRUCTURE FINALE ==="
ls -lh app/ config.py passenger_wsgi.py .env .htaccess venv/ fitgang.db 2>/dev/null | head -20

echo ""
echo "=== TERMINÉ ==="
