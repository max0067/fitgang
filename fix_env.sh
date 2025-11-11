#!/bin/bash
# Script pour corriger le fichier .env sur o2switch

cd /home/wrbh3411/fitgang.fr || exit 1

echo "🔧 Correction du fichier .env..."
echo ""

# Backup de l'ancien .env
if [ -f .env ]; then
    cp .env .env.backup
    echo "✅ Backup de l'ancien .env créé (.env.backup)"
fi

# Activer le virtualenv pour générer la SECRET_KEY
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate

# Générer une SECRET_KEY sécurisée
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Créer le nouveau .env
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

echo "✅ Nouveau fichier .env créé avec:"
echo "   - SECRET_KEY sécurisée (${SECRET_KEY:0:20}...)"
echo "   - DATABASE_URL=sqlite:///fitgang.db"
echo ""

# Vérifier que l'application charge bien le .env
echo "🧪 Test de l'application avec le nouveau .env..."
python << 'PYEOF'
import sys
sys.path.insert(0, '/home/wrbh3411/fitgang.fr')

try:
    from dotenv import load_dotenv
    load_dotenv('.env')

    from app import create_app
    app = create_app('production')

    with app.app_context():
        from app import db
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')
        secret = app.config.get('SECRET_KEY', 'NOT SET')[:30]

        print(f"✅ DATABASE_URI: {db_uri}")
        print(f"✅ SECRET_KEY: {secret}...")

        if db_uri == 'NOT SET' or 'sqlite:///fitgang.db' not in db_uri:
            print("❌ ERREUR: DATABASE_URL n'est pas chargé correctement!")
            sys.exit(1)

        print("\n✅ Configuration OK!")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo ""
    echo "🔄 Redémarrage de Passenger..."
    mkdir -p tmp
    touch tmp/restart.txt

    echo ""
    echo "✅ CORRECTION TERMINÉE!"
    echo "🌐 Va tester sur: https://fitgang.fr"
    echo ""
else
    echo ""
    echo "❌ Erreur lors du test"
    echo "⚠️  Vérifie les logs pour plus de détails"
fi
