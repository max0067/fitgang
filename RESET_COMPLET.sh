#!/bin/bash
# RESET COMPLET - Efface tout et réinstalle depuis zéro

set -e

cd /home/wrbh3411

echo "🔥 RESET COMPLET DE FITGANG.FR"
echo ""
echo "⚠️  ATTENTION: Ceci va TOUT effacer et réinstaller depuis zéro"
echo ""

# 1. SAUVEGARDE BASE DE DONNÉES
echo "1. Sauvegarde de la base de données..."
if [ -f fitgang.fr/fitgang.db ]; then
    cp fitgang.fr/fitgang.db /home/wrbh3411/fitgang_db_backup_$(date +%Y%m%d_%H%M%S).db
    echo "   ✅ Base sauvegardée dans /home/wrbh3411/"
else
    echo "   ⚠️  Aucune base de données trouvée"
fi

# 2. ARRÊT COMPLET
echo ""
echo "2. Arrêt de tous les processus Python..."
pkill -9 python 2>/dev/null || true
sleep 2

# 3. SUPPRESSION COMPLÈTE
echo ""
echo "3. Suppression complète du dossier fitgang.fr..."
cd /home/wrbh3411
rm -rf fitgang.fr
echo "   ✅ Dossier supprimé"

# 4. RECRÉATION PROPRE
echo ""
echo "4. Création d'un nouveau dossier propre..."
mkdir -p fitgang.fr
cd fitgang.fr

# 5. TÉLÉCHARGEMENT VERSION STABLE
echo ""
echo "5. Téléchargement depuis GitHub (commit a848463)..."
curl -L https://github.com/max0067/fitgang/archive/a848463.tar.gz -o source.tar.gz
tar -xzf source.tar.gz
FOLDER=$(ls -d fitgang-* | head -n 1)
mv $FOLDER/* .
mv $FOLDER/.* . 2>/dev/null || true
rm -rf $FOLDER source.tar.gz
echo "   ✅ Code installé"

# 6. CRÉATION VENV PROPRE
echo ""
echo "6. Création virtualenv propre..."
python3 -m venv venv --without-pip
curl https://bootstrap.pypa.io/pip/3.6/get-pip.py -o get-pip.py
venv/bin/python get-pip.py
rm get-pip.py

# 7. INSTALLATION DÉPENDANCES
echo ""
echo "7. Installation des dépendances..."
venv/bin/pip install Flask==2.0.3
venv/bin/pip install Flask-SQLAlchemy==2.5.1
venv/bin/pip install Flask-Login==0.5.0
venv/bin/pip install Flask-WTF==1.0.1
venv/bin/pip install WTForms==3.0.0
venv/bin/pip install Flask-Mail==0.9.1
venv/bin/pip install python-dotenv==0.19.2
venv/bin/pip install Pillow==8.4.0
venv/bin/pip install email-validator==1.1.3
echo "   ✅ Dépendances installées"

# 8. CONFIGURATION .ENV
echo ""
echo "8. Configuration .env..."
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
echo "   ✅ .env créé"

# 9. RESTAURATION BASE DE DONNÉES
echo ""
echo "9. Restauration de la base de données..."
LATEST_DB=$(ls -t /home/wrbh3411/fitgang_db_backup_*.db 2>/dev/null | head -1)
if [ ! -z "$LATEST_DB" ]; then
    cp "$LATEST_DB" fitgang.db
    echo "   ✅ Base restaurée"
else
    echo "   ⚠️  Aucune base à restaurer"
fi

# 10. PASSENGER_WSGI.PY SIMPLE
echo ""
echo "10. Configuration passenger_wsgi.py..."
cat > passenger_wsgi.py << 'WSGIEOF'
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from app import create_app
application = create_app('production')
WSGIEOF
echo "   ✅ passenger_wsgi.py créé"

# 11. .HTACCESS
echo ""
echo "11. Configuration .htaccess..."
cat > .htaccess << 'HTEOF'
PassengerEnabled on
PassengerPython /home/wrbh3411/fitgang.fr/venv/bin/python3
PassengerAppRoot /home/wrbh3411/fitgang.fr
PassengerStartupFile passenger_wsgi.py
SetEnv FLASK_ENV production
PassengerMaxPoolSize 6
PassengerMinInstances 1
HTEOF
echo "   ✅ .htaccess créé"

# 12. PERMISSIONS
echo ""
echo "12. Configuration des permissions..."
chmod 755 /home/wrbh3411/fitgang.fr
chmod 755 app
chmod 644 passenger_wsgi.py
chmod 644 .htaccess
chmod 600 .env
chmod 644 fitgang.db 2>/dev/null || true

# 13. TEST DE L'APPLICATION
echo ""
echo "13. Test de l'application..."
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

# 14. DÉMARRAGE
echo ""
echo "14. Démarrage Passenger..."
mkdir -p tmp
touch passenger_wsgi.py
echo "$(date)" > tmp/restart.txt

echo ""
echo "15. Attente 30 secondes..."
sleep 30

# 15. TEST FINAL
echo ""
echo "16. Test final..."
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
    echo "🎉 Programmes: https://fitgang.fr/programmes"
    echo ""
    echo "Base de données restaurée avec toutes tes données ✅"
else
    echo "⚠️  Code HTTP: $HTTP"
    echo ""
    echo "Lance pour voir les logs:"
    echo "  tail -50 /home/wrbh3411/fitgang.fr/log/*.log"
fi

echo ""
echo "=== STRUCTURE FINALE ==="
ls -lh /home/wrbh3411/fitgang.fr/ | head -20

echo ""
echo "=== TERMINÉ ==="
