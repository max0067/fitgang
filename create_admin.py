#!/usr/bin/env python3
"""
Script pour créer un compte administrateur FitGang
"""
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Créer la base de données si elle n'existe pas
    db.create_all()

    # Vérifier si l'admin existe déjà
    admin = User.query.filter_by(email='admin@fitgang.fr').first()

    if admin:
        print("⚠️  Un admin avec l'email admin@fitgang.fr existe déjà!")
    else:
        # Créer l'admin
        admin = User(
            email='admin@fitgang.fr',
            password_hash=generate_password_hash('admin123'),
            prenom='Admin',
            nom='FitGang',
            is_admin=True
        )

        db.session.add(admin)
        db.session.commit()

        print("✅ Compte administrateur créé avec succès!")
        print("")
        print("📧 Email: admin@fitgang.fr")
        print("🔑 Mot de passe: admin123")
        print("")
        print("⚠️  IMPORTANT: Changez ce mot de passe après la première connexion!")
