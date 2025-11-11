#!/bin/bash
# Script de diagnostic complet pour FitGang sur o2switch

echo "🔍 DIAGNOSTIC COMPLET - FITGANG"
echo "================================"
echo ""

# Aller dans le répertoire
cd /home/wrbh3411/fitgang.fr || {
    echo "❌ ERREUR CRITIQUE: Impossible de trouver /home/wrbh3411/fitgang.fr"
    exit 1
}

echo "✅ Répertoire: $(pwd)"
echo ""

# 1. Vérifier Python
echo "🐍 VÉRIFICATION PYTHON"
echo "----------------------"
which python
python --version
which python3
python3 --version
echo ""

# 2. Vérifier le virtualenv cPanel
echo "📦 VÉRIFICATION VIRTUALENV"
echo "--------------------------"
if [ -d "/home/wrbh3411/virtualenv/fitgang.fr/3.6" ]; then
    echo "✅ Virtualenv existe"
    ls -la /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/ | grep python
else
    echo "❌ Virtualenv n'existe pas!"
fi
echo ""

# 3. Activer le virtualenv et vérifier les modules
echo "📚 MODULES INSTALLÉS"
echo "--------------------"
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate
echo "Python actif: $(which python)"

python << 'PYEOF'
import sys
print(f"Version: {sys.version}")
print(f"Executable: {sys.executable}")
print("")

modules = ['dotenv', 'flask', 'flask_login', 'flask_wtf', 'flask_sqlalchemy', 'sqlalchemy']
for mod in modules:
    try:
        m = __import__(mod)
        version = getattr(m, '__version__', 'OK')
        print(f"✅ {mod}: {version}")
    except ImportError as e:
        print(f"❌ {mod}: MANQUANT")
PYEOF

echo ""

# 4. Vérifier les fichiers critiques
echo "📄 FICHIERS CRITIQUES"
echo "---------------------"
files=("passenger_wsgi.py" ".htaccess" ".env" "run.py" "app/__init__.py" "requirements.txt")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        echo "✅ $file ($size bytes)"
    else
        echo "❌ $file MANQUANT"
    fi
done
echo ""

# 5. Vérifier le contenu du .env
echo "⚙️  FICHIER .env"
echo "----------------"
if [ -f .env ]; then
    echo "Contenu (sans valeurs sensibles):"
    grep -E "^(DATABASE_URL|FLASK_ENV|FLASK_APP|BASE_URL)=" .env || echo "Variables manquantes!"

    if grep -q "DATABASE_URL=sqlite:///fitgang.db" .env; then
        echo "✅ DATABASE_URL configuré"
    else
        echo "❌ DATABASE_URL non configuré!"
    fi

    if grep -q "SECRET_KEY=" .env && ! grep -q "your-secret-key-here" .env; then
        echo "✅ SECRET_KEY configuré"
    else
        echo "❌ SECRET_KEY non configuré!"
    fi
else
    echo "❌ Fichier .env n'existe pas!"
fi
echo ""

# 6. Vérifier passenger_wsgi.py
echo "🚀 PASSENGER_WSGI.PY"
echo "--------------------"
if [ -f passenger_wsgi.py ]; then
    echo "Premières lignes:"
    head -20 passenger_wsgi.py
    echo "..."

    if grep -q "def application(environ, start_response):" passenger_wsgi.py; then
        echo "✅ Fonction application() trouvée"
    else
        echo "❌ Fonction application() manquante!"
    fi

    if grep -q "from dotenv import load_dotenv" passenger_wsgi.py; then
        echo "✅ Import dotenv OK"
    else
        echo "❌ Import dotenv manquant!"
    fi
else
    echo "❌ passenger_wsgi.py n'existe pas!"
fi
echo ""

# 7. Vérifier .htaccess
echo "⚙️  .HTACCESS"
echo "-------------"
if [ -f .htaccess ]; then
    cat .htaccess
else
    echo "❌ .htaccess n'existe pas!"
fi
echo ""

# 8. Tester le chargement de l'application
echo "🧪 TEST APPLICATION FLASK"
echo "-------------------------"
python << 'PYEOF'
import sys
import os
import traceback

sys.path.insert(0, '/home/wrbh3411/fitgang.fr')
os.chdir('/home/wrbh3411/fitgang.fr')

try:
    print("1. Import dotenv...")
    from dotenv import load_dotenv
    print("   ✅ dotenv importé")

    print("2. Chargement .env...")
    load_dotenv('.env')
    print("   ✅ .env chargé")

    print("3. Import create_app...")
    from app import create_app
    print("   ✅ create_app importé")

    print("4. Création de l'application...")
    app = create_app('production')
    print("   ✅ Application créée")

    print("5. Vérification configuration...")
    with app.app_context():
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')
        secret = app.config.get('SECRET_KEY', 'NOT SET')[:30]
        print(f"   DATABASE_URI: {db_uri}")
        print(f"   SECRET_KEY: {secret}...")

        if 'NOT SET' in db_uri:
            print("   ❌ DATABASE_URI non configuré!")
        else:
            print("   ✅ Configuration OK")

    print("\n✅ APPLICATION FONCTIONNE EN PYTHON!")
    print("Le problème est probablement dans Passenger/Apache")

except Exception as e:
    print(f"\n❌ ERREUR LORS DU CHARGEMENT:")
    print(traceback.format_exc())
PYEOF

echo ""

# 9. Vérifier les permissions
echo "🔒 PERMISSIONS"
echo "--------------"
ls -la passenger_wsgi.py .htaccess .env 2>/dev/null || echo "Fichiers manquants"
echo ""

# 10. Vérifier les logs (si disponibles)
echo "📋 LOGS (dernières lignes)"
echo "--------------------------"
if [ -f ~/logs/error.log ]; then
    echo "Dernières erreurs:"
    tail -20 ~/logs/error.log
else
    echo "⚠️  Logs non trouvés dans ~/logs/error.log"
fi
echo ""

# 11. Vérifier le répertoire tmp
echo "📁 RÉPERTOIRE TMP"
echo "-----------------"
if [ -d tmp ]; then
    ls -la tmp/
else
    echo "⚠️  Répertoire tmp n'existe pas"
    echo "Création..."
    mkdir -p tmp
fi
echo ""

echo "================================"
echo "🏁 DIAGNOSTIC TERMINÉ"
echo "================================"
echo ""
echo "Maintenant, lance le script de réparation: ./repair_all.sh"
