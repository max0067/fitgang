#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script simple pour diagnostiquer le problème d'envoi d'emails
"""
print("=" * 60)
print("DIAGNOSTIC EMAIL FITGANG")
print("=" * 60)

# 1. Vérifier l'import de Flask-Mail
print("\n1. Import Flask-Mail:")
try:
    import flask_mail
    print(f"   ✓ Flask-Mail installé (version {flask_mail.__version__})")
except ImportError as e:
    print(f"   ✗ PROBLÈME: Flask-Mail n'est pas installé!")
    print(f"   Erreur: {e}")
    print("\n   SOLUTION: pip install Flask-Mail")
    exit(1)

# 2. Vérifier l'import de l'application
print("\n2. Import de l'application:")
try:
    from app import create_app, mail, MAIL_ENABLED
    print("   ✓ Application importée")
    print(f"   MAIL_ENABLED = {MAIL_ENABLED}")
    print(f"   mail object = {mail}")
except Exception as e:
    print(f"   ✗ PROBLÈME lors de l'import: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# 3. Créer l'application
print("\n3. Création de l'application:")
try:
    app = create_app('production')
    print("   ✓ Application créée")
except Exception as e:
    print(f"   ✗ PROBLÈME: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# 4. Vérifier la configuration
print("\n4. Configuration email:")
with app.app_context():
    print(f"   MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"   MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"   MAIL_USE_SSL: {app.config.get('MAIL_USE_SSL')}")
    print(f"   MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    print(f"   MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    print(f"   MAIL_PASSWORD: {'***' if app.config.get('MAIL_PASSWORD') else 'NON DÉFINI'}")
    print(f"   MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER')}")

# 5. Test de connexion SMTP
print("\n5. Test de connexion SMTP:")
try:
    import smtplib
    import ssl

    server = app.config.get('MAIL_SERVER')
    port = app.config.get('MAIL_PORT')
    username = app.config.get('MAIL_USERNAME')
    password = app.config.get('MAIL_PASSWORD')

    print(f"   Connexion à {server}:{port}...")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(server, port, context=context, timeout=10) as smtp:
        print("   ✓ Connexion SSL établie")
        smtp.login(username, password)
        print("   ✓ Authentification réussie")

except Exception as e:
    print(f"   ✗ PROBLÈME de connexion SMTP: {e}")
    import traceback
    traceback.print_exc()

# 6. Test d'envoi avec Flask-Mail
print("\n6. Test d'envoi avec Flask-Mail:")
try:
    with app.app_context():
        from flask_mail import Message

        if not mail:
            print("   ✗ PROBLÈME: mail object n'est pas initialisé")
            print("   Vérifiez que Flask-Mail est bien initialisé dans app/__init__.py")
            exit(1)

        msg = Message(
            subject="Test FitGang - Diagnostic Email",
            recipients=[app.config.get('ADMIN_EMAIL')],
            body="Ceci est un email de test du script de diagnostic."
        )
        msg.html = "<p><strong>Email de test OK!</strong></p>"

        print(f"   Envoi à: {app.config.get('ADMIN_EMAIL')}")
        mail.send(msg)
        print("   ✓ EMAIL ENVOYÉ AVEC SUCCÈS!")

except Exception as e:
    print(f"   ✗ ERREUR lors de l'envoi: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("FIN DU DIAGNOSTIC")
print("=" * 60)
