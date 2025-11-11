#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de diagnostic pour vérifier la configuration des emails
À lancer sur le serveur pour diagnostiquer pourquoi les emails ne partent pas
"""
import os
import sys
from dotenv import load_dotenv

print("=" * 70)
print("DIAGNOSTIC CONFIGURATION EMAIL FITGANG")
print("=" * 70)

# Charger .env
load_dotenv()

print("\n1. VARIABLES D'ENVIRONNEMENT")
print("-" * 70)
mail_vars = {
    'MAIL_SERVER': os.getenv('MAIL_SERVER'),
    'MAIL_PORT': os.getenv('MAIL_PORT'),
    'MAIL_USE_SSL': os.getenv('MAIL_USE_SSL'),
    'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
    'MAIL_PASSWORD': '***' if os.getenv('MAIL_PASSWORD') else 'NOT SET',
    'MAIL_DEFAULT_SENDER': os.getenv('MAIL_DEFAULT_SENDER'),
    'ADMIN_EMAIL': os.getenv('ADMIN_EMAIL'),
}

all_set = True
for key, value in mail_vars.items():
    status = "✓" if value and value != 'NOT SET' else "✗"
    print(f"   {status} {key:25s} = {value}")
    if not value or value == 'NOT SET':
        all_set = False

if not all_set:
    print("\n⚠️  PROBLÈME: Certaines variables email ne sont pas définies dans .env!")
    print("   → Ajoute-les dans le fichier .env (voir CONFIGURER_EMAILS.md)")
    sys.exit(1)

print("\n2. IMPORT FLASK-MAIL")
print("-" * 70)
try:
    from flask_mail import Mail, Message
    print("   ✓ Flask-Mail importé avec succès")
except ImportError as e:
    print(f"   ✗ ERREUR: Flask-Mail n'est pas installé!")
    print(f"   → Exécute: pip install Flask-Mail==0.10.0")
    sys.exit(1)

print("\n3. CRÉATION DE L'APPLICATION FLASK")
print("-" * 70)
try:
    from app import create_app, MAIL_ENABLED, mail
    app = create_app('production')
    print(f"   ✓ Application créée")
    print(f"   ✓ MAIL_ENABLED = {MAIL_ENABLED}")

    if not MAIL_ENABLED:
        print("   ✗ MAIL_ENABLED est False - Flask-Mail non activé!")
        sys.exit(1)

    if not mail:
        print("   ✗ L'objet 'mail' est None - Flask-Mail non initialisé!")
        sys.exit(1)

    print(f"   ✓ Objet mail initialisé")

except Exception as e:
    print(f"   ✗ ERREUR lors de la création de l'app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n4. CONFIGURATION FLASK-MAIL DANS L'APP")
print("-" * 70)
with app.app_context():
    config_keys = ['MAIL_SERVER', 'MAIL_PORT', 'MAIL_USE_SSL', 'MAIL_USERNAME', 'MAIL_DEFAULT_SENDER']
    for key in config_keys:
        value = app.config.get(key)
        if key == 'MAIL_PASSWORD':
            value = '***' if value else 'NOT SET'
        status = "✓" if value else "✗"
        print(f"   {status} {key:25s} = {value}")

print("\n5. TEST D'ENVOI D'EMAIL")
print("-" * 70)
test_email = os.getenv('ADMIN_EMAIL', 'admin@fitgang.fr')
print(f"   Tentative d'envoi à: {test_email}")

try:
    with app.app_context():
        msg = Message(
            subject="[TEST] Configuration Email FitGang",
            recipients=[test_email],
            body="Ceci est un email de test. Si tu reçois ce message, la configuration email fonctionne!"
        )
        msg.html = """
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #dc3545;">✓ Configuration Email OK!</h2>
            <p>Si tu reçois ce message, cela signifie que:</p>
            <ul>
                <li>✓ Flask-Mail est installé</li>
                <li>✓ Les variables d'environnement sont correctes</li>
                <li>✓ La connexion SMTP fonctionne</li>
            </ul>
            <p>Tu peux maintenant envoyer des emails depuis FitGang!</p>
            <hr>
            <small>Email envoyé depuis test_mail_config.py</small>
        </body>
        </html>
        """

        mail.send(msg)
        print(f"   ✓ EMAIL ENVOYÉ AVEC SUCCÈS!")
        print(f"   → Vérifie ta boîte mail: {test_email}")

except Exception as e:
    print(f"   ✗ ERREUR lors de l'envoi: {e}")
    import traceback
    traceback.print_exc()
    print("\n   CAUSES POSSIBLES:")
    print("   1. Mauvais mot de passe email")
    print("   2. Serveur SMTP mail.fitgang.fr non accessible")
    print("   3. Port 465 bloqué")
    print("   4. Email admin@fitgang.fr n'existe pas sur le serveur")
    sys.exit(1)

print("\n6. TEST DE SEND_WELCOME_EMAIL")
print("-" * 70)
try:
    with app.app_context():
        from app.email import send_welcome_email
        from app.models import User

        # Créer un utilisateur fictif pour le test
        class FakeUser:
            def __init__(self):
                self.prenom = "Test"
                self.nom = "User"
                self.email = test_email

        fake_user = FakeUser()
        print(f"   Test d'envoi à: {fake_user.email}")

        result = send_welcome_email(fake_user)

        if result:
            print(f"   ✓ EMAIL DE BIENVENUE ENVOYÉ!")
            print(f"   → Vérifie ta boîte mail: {test_email}")
        else:
            print(f"   ✗ L'envoi a échoué (send_welcome_email a retourné False)")

except Exception as e:
    print(f"   ✗ ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("DIAGNOSTIC TERMINÉ")
print("=" * 70)

if all_set:
    print("\n✓ TOUT EST OK! Les emails devraient fonctionner maintenant.")
    print("\nPROCHAINE ÉTAPE:")
    print("  → Teste en créant un nouveau compte sur fitgang.fr")
    print("  → Tu devrais recevoir un email de bienvenue!")
else:
    print("\n✗ Il y a des problèmes à corriger (voir ci-dessus)")
