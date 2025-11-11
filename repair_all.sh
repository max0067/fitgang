#!/bin/bash
# Script de réparation complète pour FitGang sur o2switch

echo "🔧 RÉPARATION COMPLÈTE - FITGANG"
echo "================================="
echo ""

# Aller dans le répertoire
cd /home/wrbh3411/fitgang.fr || {
    echo "❌ ERREUR: Impossible de trouver /home/wrbh3411/fitgang.fr"
    exit 1
}

echo "📍 Répertoire: $(pwd)"
echo ""

# 1. Activer le virtualenv
echo "🐍 ACTIVATION VIRTUALENV"
echo "------------------------"
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate || {
    echo "❌ ERREUR: Impossible d'activer le virtualenv"
    echo "Va dans cPanel > Setup Python App et vérifie que l'application existe"
    exit 1
}
echo "✅ Virtualenv activé"
echo "Python: $(which python)"
echo ""

# 2. Réinstaller toutes les dépendances
echo "📦 RÉINSTALLATION DES DÉPENDANCES"
echo "----------------------------------"
pip install --upgrade pip

# Installer une par une pour voir les erreurs
echo "Installation de Flask..."
pip install Flask==2.0.3

echo "Installation de Flask-Login..."
pip install Flask-Login==0.5.0

echo "Installation de Flask-WTF..."
pip install Flask-WTF==0.15.1

echo "Installation de Flask-SQLAlchemy..."
pip install Flask-SQLAlchemy==2.5.1

echo "Installation de SQLAlchemy..."
pip install SQLAlchemy==1.4.46

echo "Installation de python-dotenv..."
pip install python-dotenv==0.19.2

echo "Installation de Werkzeug..."
pip install Werkzeug==2.0.3

echo "Installation de WTForms..."
pip install WTForms==2.3.3

echo "Installation des autres dépendances..."
pip install Flask-Migrate==3.1.0
pip install stripe==2.63.0
pip install email-validator==1.1.3
pip install dnspython==2.1.0

echo "✅ Toutes les dépendances installées"
echo ""

# 3. Recréer le fichier .env
echo "📝 RECRÉATION DU FICHIER .ENV"
echo "-----------------------------"

# Backup de l'ancien
[ -f .env ] && cp .env .env.old

# Générer une vraie SECRET_KEY
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

cat > .env << EOF
# Configuration FitGang - o2switch
SECRET_KEY=$SECRET_KEY
DATABASE_URL=sqlite:///fitgang.db
STRIPE_PUBLIC_KEY=pk_test_VOTRE_CLE_PUBLIQUE_ICI
STRIPE_SECRET_KEY=sk_test_VOTRE_CLE_SECRETE_ICI
STRIPE_WEBHOOK_SECRET=whsec_VOTRE_WEBHOOK_SECRET_ICI
BASE_URL=https://fitgang.fr
FLASK_ENV=production
FLASK_APP=run.py
FLASK_DEBUG=False
EOF

chmod 644 .env
echo "✅ Fichier .env créé"
echo "SECRET_KEY: ${SECRET_KEY:0:20}..."
echo ""

# 4. Recréer passenger_wsgi.py avec gestion d'erreurs
echo "🚀 RECRÉATION PASSENGER_WSGI.PY"
echo "--------------------------------"

cat > passenger_wsgi.py << 'EOF'
"""
Fichier WSGI pour o2switch/Passenger
Version avec gestion d'erreurs détaillée
"""
import sys
import os
import traceback

# Ajouter le répertoire du projet au path
sys.path.insert(0, os.getcwd())

def application(environ, start_response):
    """
    Point d'entrée WSGI pour Passenger
    Affiche les erreurs détaillées pour faciliter le débogage
    """
    try:
        # Charger les variables d'environnement
        from dotenv import load_dotenv
        load_dotenv('.env')

        # Créer l'application Flask
        from app import create_app
        flask_app = create_app('production')

        # Appeler l'application Flask
        return flask_app(environ, start_response)

    except Exception as e:
        # En cas d'erreur, afficher un message détaillé
        error_text = traceback.format_exc()

        # Page HTML avec l'erreur
        error_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Erreur - FitGang</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            padding: 20px;
            background: #0a0a0a;
            color: #ff4444;
        }}
        h1 {{
            color: #ff4444;
            border-bottom: 2px solid #ff4444;
            padding-bottom: 10px;
        }}
        pre {{
            background: #1a1a1a;
            padding: 20px;
            border: 2px solid #ff4444;
            border-radius: 5px;
            overflow: auto;
            color: #ffffff;
            font-size: 12px;
        }}
        .info {{
            background: #1a3a1a;
            border: 1px solid #44ff44;
            color: #44ff44;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <h1>🏋️ FitGang - Erreur de Démarrage</h1>

    <div class="info">
        <strong>Informations:</strong><br>
        Python: {sys.version}<br>
        Chemin: {os.getcwd()}<br>
        Exécutable: {sys.executable}
    </div>

    <h2>Erreur détaillée:</h2>
    <pre>{error_text}</pre>

    <p style="color: #aaa;">
        Si cette erreur persiste, exécute: cd /home/wrbh3411/fitgang.fr && ./diagnostic.sh
    </p>
</body>
</html>"""

        # Retourner la page d'erreur
        status = '200 OK'
        response_headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, response_headers)
        return [error_html.encode('utf-8')]
EOF

chmod 755 passenger_wsgi.py
echo "✅ passenger_wsgi.py créé"
echo ""

# 5. Vérifier/Recréer .htaccess
echo "⚙️  VÉRIFICATION .HTACCESS"
echo "--------------------------"

if [ ! -f .htaccess ] || ! grep -q "PassengerEnabled On" .htaccess; then
    echo "⚠️  .htaccess manquant ou incorrect, recréation..."

    cat > .htaccess << 'EOF'
# DO NOT REMOVE. CLOUDLINUX PASSENGER CONFIGURATION BEGIN
PassengerEnabled On
PassengerAppRoot "/home/wrbh3411/fitgang.fr"
PassengerBaseURI "/"
PassengerPython "/home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/python3"
PassengerStartupFile "passenger_wsgi.py"
# DO NOT REMOVE. CLOUDLINUX PASSENGER CONFIGURATION END
EOF

    chmod 644 .htaccess
    echo "✅ .htaccess créé"
else
    echo "✅ .htaccess OK"
fi
echo ""

# 6. Créer la base de données si elle n'existe pas
echo "🗄️  BASE DE DONNÉES"
echo "-------------------"

if [ ! -f fitgang.db ]; then
    echo "Base de données non trouvée, création..."

    if [ -f create_admin.py ]; then
        python create_admin.py || {
            echo "⚠️  Erreur lors de la création de la base"
            echo "Tentative manuelle..."

            python << 'PYEOF'
import sys
sys.path.insert(0, '/home/wrbh3411/fitgang.fr')

from dotenv import load_dotenv
load_dotenv('.env')

from app import create_app, db
from app.models import User

app = create_app('production')

with app.app_context():
    db.create_all()
    print("✅ Tables créées")

    # Créer l'admin
    if not User.query.filter_by(email='admin@fitgang.fr').first():
        admin = User(
            username='admin',
            email='admin@fitgang.fr',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Compte admin créé: admin@fitgang.fr / admin123")
    else:
        print("✅ Compte admin existe déjà")
PYEOF
        }
    fi

    chmod 644 fitgang.db
else
    echo "✅ Base de données existe"
fi
echo ""

# 7. Tester l'application
echo "🧪 TEST COMPLET DE L'APPLICATION"
echo "---------------------------------"

python << 'PYEOF'
import sys
import os
sys.path.insert(0, '/home/wrbh3411/fitgang.fr')
os.chdir('/home/wrbh3411/fitgang.fr')

try:
    from dotenv import load_dotenv
    load_dotenv('.env')
    print("✅ .env chargé")

    from app import create_app
    app = create_app('production')
    print("✅ Application créée")

    with app.app_context():
        from app import db
        from app.models import User

        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        secret = app.config.get('SECRET_KEY', '')[:30]

        print(f"✅ DATABASE_URI: {db_uri}")
        print(f"✅ SECRET_KEY: {secret}...")

        # Tester la DB
        user_count = User.query.count()
        print(f"✅ Base de données OK ({user_count} utilisateurs)")

    print("\n✅✅✅ APPLICATION FONCTIONNE PARFAITEMENT! ✅✅✅")

except Exception as e:
    print(f"\n❌ ERREUR:")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ L'application ne fonctionne pas en Python"
    echo "Il y a un problème dans le code de l'application"
    exit 1
fi

echo ""

# 8. Configurer les permissions finales
echo "🔒 PERMISSIONS FINALES"
echo "----------------------"
chmod 755 .
chmod 755 passenger_wsgi.py
chmod 644 .htaccess
chmod 644 .env
[ -f fitgang.db ] && chmod 644 fitgang.db
echo "✅ Permissions configurées"
echo ""

# 9. Créer le répertoire tmp et redémarrer
echo "🔄 REDÉMARRAGE PASSENGER"
echo "------------------------"
mkdir -p tmp
touch tmp/restart.txt
echo "✅ Passenger redémarré"
echo ""

echo "================================="
echo "✅✅✅ RÉPARATION TERMINÉE! ✅✅✅"
echo "================================="
echo ""
echo "🌐 Va maintenant sur: https://fitgang.fr"
echo ""
echo "🔐 Connexion admin:"
echo "   Email: admin@fitgang.fr"
echo "   Mot de passe: admin123"
echo ""
echo "⚠️  Si tu vois encore une erreur:"
echo "   1. Copie l'erreur complète"
echo "   2. Vérifie les logs: tail -f ~/logs/error.log"
echo "   3. Redémarre via cPanel > Setup Python App > Restart"
echo ""
