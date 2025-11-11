#!/bin/bash
# Script simple pour créer le compte admin

cd /home/wrbh3411/fitgang.fr
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate

echo "🔐 Création du compte administrateur..."
echo ""

python << 'PYEOF'
import sys
sys.path.insert(0, '/home/wrbh3411/fitgang.fr')

from dotenv import load_dotenv
load_dotenv('.env')

from app import create_app, db
from app.models import User

app = create_app('production')

with app.app_context():
    # Vérifier si l'admin existe déjà
    admin = User.query.filter_by(email='admin@fitgang.fr').first()

    if admin:
        print("⚠️  Le compte admin existe déjà!")
        print("")
        print("📧 Email: admin@fitgang.fr")
        print("🔑 Mot de passe: admin123")
        print("")
        print("Si tu as oublié le mot de passe, supprime la base de données et relance ce script.")
    else:
        # Créer le compte admin
        admin = User(
            username='admin',
            email='admin@fitgang.fr',
            is_admin=True
        )
        admin.set_password('admin123')

        db.session.add(admin)
        db.session.commit()

        print("✅ Compte administrateur créé avec succès!")
        print("")
        print("🔐 Identifiants de connexion:")
        print("   📧 Email: admin@fitgang.fr")
        print("   🔑 Mot de passe: admin123")
        print("")
        print("⚠️  IMPORTANT: Change ce mot de passe après ta première connexion!")
        print("")
        print("🌐 Connecte-toi sur: https://fitgang.fr/login")
PYEOF

echo ""
echo "✅ Terminé!"
