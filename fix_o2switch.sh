#!/bin/bash
# Script à exécuter SUR O2SWITCH via SSH
# Ce script installe les dépendances compatibles Python 3.6

echo "🔧 FIX FITGANG sur O2SWITCH"
echo "============================"
echo ""

# Aller dans le répertoire du projet
cd /home/wrbh3411/fitgang.fr || {
    echo "❌ Erreur: Impossible de trouver /home/wrbh3411/fitgang.fr"
    exit 1
}

echo "📍 Répertoire: $(pwd)"
echo ""

# Activer le virtualenv cPanel
echo "🐍 Activation du virtualenv cPanel..."
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate || {
    echo "❌ Erreur: Impossible d'activer le virtualenv"
    echo "Vérifiez que le virtualenv existe dans cPanel > Setup Python App"
    exit 1
}

echo "✅ Virtualenv activé"
echo "📍 Python: $(which python)"
echo "📍 Pip: $(which pip)"
echo ""

# Mettre à jour pip
echo "📦 Mise à jour de pip..."
pip install --upgrade pip

# Installer les dépendances compatibles Python 3.6
echo ""
echo "📦 Installation des dépendances Python 3.6 compatibles..."
pip install Flask==2.0.3
pip install Flask-Login==0.5.0
pip install Flask-WTF==0.15.1
pip install Flask-Migrate==3.1.0
pip install Flask-SQLAlchemy==2.5.1
pip install SQLAlchemy==1.4.46
pip install python-dotenv==0.19.2
pip install Werkzeug==2.0.3
pip install WTForms==2.3.3
pip install stripe==2.63.0
pip install email-validator==1.1.3
pip install dnspython==2.1.0

echo ""
echo "✅ Vérification des installations..."
python -c "import dotenv; print('✅ python-dotenv:', dotenv.__version__)" || echo "❌ python-dotenv manquant"
python -c "import flask; print('✅ Flask:', flask.__version__)" || echo "❌ Flask manquant"
python -c "import flask_login; print('✅ Flask-Login OK')" || echo "❌ Flask-Login manquant"
python -c "import flask_wtf; print('✅ Flask-WTF OK')" || echo "❌ Flask-WTF manquant"
python -c "import flask_sqlalchemy; print('✅ Flask-SQLAlchemy OK')" || echo "❌ Flask-SQLAlchemy manquant"

# Vérifier/Créer le fichier .env
echo ""
if [ ! -f .env ]; then
    echo "📝 Création du fichier .env..."

    # Générer une SECRET_KEY sécurisée
    SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

    cat > .env << EOF
# Configuration de production pour O2Switch
SECRET_KEY=$SECRET_KEY

# Base de données SQLite
DATABASE_URL=sqlite:///fitgang.db

# Clés Stripe (à remplacer par tes vraies clés)
STRIPE_PUBLIC_KEY=pk_test_VOTRE_CLE_PUBLIQUE_ICI
STRIPE_SECRET_KEY=sk_test_VOTRE_CLE_SECRETE_ICI
STRIPE_WEBHOOK_SECRET=whsec_VOTRE_WEBHOOK_SECRET_ICI

# URL de base
BASE_URL=https://fitgang.fr

# Environnement
FLASK_ENV=production
FLASK_APP=run.py
FLASK_DEBUG=False
EOF

    echo "✅ Fichier .env créé avec SECRET_KEY sécurisée"
else
    echo "✅ Le fichier .env existe déjà"
fi

# Tester le chargement de l'application
echo ""
echo "🧪 Test du chargement de l'application..."
python << 'PYEOF'
import sys
sys.path.insert(0, '/home/wrbh3411/fitgang.fr')

try:
    from dotenv import load_dotenv
    load_dotenv('.env')
    print("✅ Fichier .env chargé")

    from app import create_app
    app = create_app('production')
    print("✅ Application Flask créée avec succès!")

    # Vérifier la configuration
    with app.app_context():
        from app import db
        print(f"✅ Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')}")
        print(f"✅ Secret Key: {app.config.get('SECRET_KEY', 'NOT SET')[:20]}...")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Application testée avec succès!"
else
    echo ""
    echo "❌ Erreur lors du test de l'application"
    exit 1
fi

# Vérifier si la base de données existe
echo ""
if [ ! -f fitgang.db ]; then
    echo "🗄️  Base de données non trouvée, création..."
    python create_admin.py || {
        echo "⚠️  Attention: Erreur lors de la création de la base de données"
        echo "Tu pourras la créer manuellement plus tard avec: python create_admin.py"
    }
else
    echo "✅ Base de données fitgang.db existe déjà"
fi

# Configurer les permissions
echo ""
echo "🔒 Configuration des permissions..."
chmod 755 passenger_wsgi.py
chmod 644 .htaccess
if [ -f fitgang.db ]; then
    chmod 644 fitgang.db
fi

# Redémarrer Passenger
echo ""
echo "🔄 Redémarrage de Passenger..."
mkdir -p tmp
touch tmp/restart.txt

echo ""
echo "🎉 INSTALLATION TERMINÉE AVEC SUCCÈS!"
echo "======================================"
echo ""
echo "🌐 Va maintenant sur: https://fitgang.fr"
echo ""
echo "🔐 Identifiants admin par défaut:"
echo "   📧 Email: admin@fitgang.fr"
echo "   🔑 Mot de passe: admin123"
echo ""
echo "⚠️  CHANGE CE MOT DE PASSE après ta première connexion!"
echo ""
echo "📝 Si tu vois encore une erreur, regarde les logs:"
echo "   tail -f ~/logs/error.log"
echo ""
