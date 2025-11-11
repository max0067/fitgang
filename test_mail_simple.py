#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test SMTP direct pour voir exactement ce qui se passe
"""
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv('.env')

print("=" * 60)
print("TEST SMTP DIRECT")
print("=" * 60)

# Configuration
smtp_server = os.getenv('MAIL_SERVER')
smtp_port = int(os.getenv('MAIL_PORT'))
username = os.getenv('MAIL_USERNAME')
password = os.getenv('MAIL_PASSWORD')
from_email = os.getenv('MAIL_DEFAULT_SENDER')

print(f"\nConfiguration:")
print(f"  Serveur: {smtp_server}:{smtp_port}")
print(f"  Username: {username}")
print(f"  From: {from_email}")
print(f"  Password: {'***' if password else 'NON DÉFINI'}")

# Demander l'email de destination
to_email = input(f"\n📧 Email de destination (défaut: {username}): ").strip()
if not to_email:
    to_email = username

print(f"\n{'=' * 60}")
print("ENVOI D'UN EMAIL DE TEST")
print(f"{'=' * 60}\n")

try:
    # Créer le message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'TEST SMTP Direct - FitGang'
    msg['From'] = from_email
    msg['To'] = to_email

    # Version texte
    text_content = """
    Ceci est un email de test envoyé directement via SMTP.

    Si vous recevez cet email, cela signifie que la configuration SMTP fonctionne.

    Test effectué par FitGang
    """

    # Version HTML
    html_content = """
    <html>
      <body>
        <h1 style="color: #dc3545;">TEST SMTP Direct - FitGang</h1>
        <p>Ceci est un email de test envoyé <strong>directement via SMTP</strong>.</p>
        <p>Si vous recevez cet email, cela signifie que la configuration SMTP fonctionne.</p>
        <hr>
        <p><em>Test effectué par FitGang</em></p>
      </body>
    </html>
    """

    # Ajouter les parties
    part1 = MIMEText(text_content, 'plain')
    part2 = MIMEText(html_content, 'html')
    msg.attach(part1)
    msg.attach(part2)

    print(f"1. Connexion au serveur SMTP {smtp_server}:{smtp_port}...")
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context, timeout=30) as server:
        print("   ✓ Connexion SSL établie")

        print(f"\n2. Authentification avec {username}...")
        server.login(username, password)
        print("   ✓ Authentification réussie")

        print(f"\n3. Envoi de l'email à {to_email}...")
        result = server.send_message(msg)
        print("   ✓ Email envoyé au serveur SMTP!")

        if result:
            print(f"\n⚠️  Certains destinataires ont été refusés:")
            for addr, (code, message) in result.items():
                print(f"   - {addr}: {code} {message}")
        else:
            print("\n✅ SUCCÈS COMPLET!")
            print(f"\n📧 Email envoyé à: {to_email}")
            print(f"   De: {from_email}")
            print(f"   Sujet: TEST SMTP Direct - FitGang")

    print(f"\n{'=' * 60}")
    print("IMPORTANT:")
    print(f"{'=' * 60}")
    print(f"1. Vérifiez votre boîte mail: {to_email}")
    print(f"2. Vérifiez aussi les SPAMS / Courrier indésirable")
    print(f"3. Si l'email n'arrive pas, le problème vient de:")
    print(f"   - Votre serveur mail {smtp_server} qui n'envoie pas vraiment")
    print(f"   - Un filtre anti-spam qui bloque vos emails")
    print(f"   - Une configuration SPF/DKIM manquante sur fitgang.fr")

except smtplib.SMTPAuthenticationError as e:
    print(f"\n✗ ERREUR D'AUTHENTIFICATION: {e}")
    print("   Vérifiez votre nom d'utilisateur et mot de passe")

except smtplib.SMTPException as e:
    print(f"\n✗ ERREUR SMTP: {e}")

except Exception as e:
    print(f"\n✗ ERREUR: {e}")
    import traceback
    traceback.print_exc()

print(f"\n{'=' * 60}")
