#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier l'envoi d'emails
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

print("=" * 60)
print("TEST CONFIGURATION EMAIL")
print("=" * 60)

# Vérifier les variables d'environnement
print("\n1. Variables d'environnement:")
print(f"   MAIL_SERVER: {os.getenv('MAIL_SERVER')}")
print(f"   MAIL_PORT: {os.getenv('MAIL_PORT')}")
print(f"   MAIL_USE_SSL: {os.getenv('MAIL_USE_SSL')}")
print(f"   MAIL_USERNAME: {os.getenv('MAIL_USERNAME')}")
print(f"   MAIL_PASSWORD: {'***' if os.getenv('MAIL_PASSWORD') else 'NOT SET'}")
print(f"   MAIL_DEFAULT_SENDER: {os.getenv('MAIL_DEFAULT_SENDER')}")

# Tester l'import de Flask-Mail
print("\n2. Import Flask-Mail:")
try:
    from flask_mail import Mail, Message
    print("   ✓ Flask-Mail importé avec succès")
except ImportError as e:
    print(f"   ✗ Erreur: {e}")
    exit(1)

# Tester la création de l'application
print("\n3. Création de l'application Flask:")
try:
    from app import create_app
    app = create_app('production')
    print("   ✓ Application créée avec succès")
except Exception as e:
    print(f"   ✗ Erreur: {e}")
    exit(1)

# Vérifier la configuration de Mail
print("\n4. Configuration Flask-Mail dans l'app:")
print(f"   MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
print(f"   MAIL_PORT: {app.config.get('MAIL_PORT')}")
print(f"   MAIL_USE_SSL: {app.config.get('MAIL_USE_SSL')}")
print(f"   MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")

# Vérifier si Mail est initialisé
print("\n5. Vérification de Mail:")
try:
    from app import mail, MAIL_ENABLED
    print(f"   MAIL_ENABLED: {MAIL_ENABLED}")
    if mail:
        print("   ✓ Mail object initialisé")
    else:
        print("   ✗ Mail object est None")
except Exception as e:
    print(f"   ✗ Erreur: {e}")

# Test d'envoi d'email
print("\n6. Test d'envoi d'email:")
try:
    with app.app_context():
        from app import mail

        if not mail:
            print("   ✗ Mail n'est pas initialisé")
            exit(1)

        # Créer un message de test
        msg = Message(
            subject="Test FitGang Email",
            recipients=[os.getenv('ADMIN_EMAIL', 'admin@fitgang.fr')],
            body="Ceci est un email de test depuis FitGang."
        )
        msg.html = "<p><strong>Ceci est un email de test depuis FitGang.</strong></p>"

        print(f"   Envoi à: {os.getenv('ADMIN_EMAIL', 'admin@fitgang.fr')}")
        mail.send(msg)
        print("   ✓ Email envoyé avec succès!")

except Exception as e:
    print(f"   ✗ Erreur lors de l'envoi: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("FIN DU TEST")
print("=" * 60)
