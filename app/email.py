"""
Gestion des emails pour l'application FitGang
Envoi d'emails pour bienvenue, confirmation d'achat, et notifications admin
"""
import os
from flask import render_template, current_app
from flask_mail import Message
from app import mail


def send_email(subject, recipient, text_body, html_body):
    """
    Fonction générique pour envoyer un email
    """
    msg = Message(subject, recipients=[recipient])
    msg.body = text_body
    msg.html = html_body

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return False


def send_welcome_email(user):
    """
    Envoie un email de bienvenue lors de l'inscription
    """
    subject = "Bienvenue sur FitGang! 💪"

    text_body = f"""
Salut {user.prenom}!

Bienvenue dans la communauté FitGang! 🎉

Nous sommes ravis de t'accueillir parmi nous. Tu as maintenant accès à:
- Des programmes d'entraînement personnalisés
- Des ebooks nutrition et fitness
- Des compléments alimentaires recommandés
- Un suivi de tes progrès

N'hésite pas à explorer nos programmes et à commencer ton parcours vers tes objectifs!

À très vite,
L'équipe FitGang
"""

    html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #dc3545; border-bottom: 3px solid #dc3545; padding-bottom: 10px;">
            Bienvenue sur FitGang! 💪
        </h1>

        <p>Salut <strong>{user.prenom}</strong>!</p>

        <p>Nous sommes ravis de t'accueillir dans la communauté FitGang! 🎉</p>

        <p>Tu as maintenant accès à:</p>
        <ul>
            <li>Des programmes d'entraînement personnalisés</li>
            <li>Des ebooks nutrition et fitness</li>
            <li>Des compléments alimentaires recommandés</li>
            <li>Un suivi de tes progrès</li>
        </ul>

        <p style="margin-top: 30px;">
            <a href="https://fitgang.fr/programmes"
               style="background-color: #dc3545; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                Découvrir nos programmes
            </a>
        </p>

        <p style="margin-top: 30px; color: #666; font-size: 14px;">
            À très vite,<br>
            <strong>L'équipe FitGang</strong>
        </p>
    </div>
</body>
</html>
"""

    return send_email(subject, user.email, text_body, html_body)


def send_purchase_confirmation_email(user, item, item_type):
    """
    Envoie un email de confirmation d'achat à l'utilisateur
    """
    # Déterminer le nom du produit
    item_name = getattr(item, 'titre', None) or getattr(item, 'nom', 'Produit')

    type_labels = {
        'programme': 'Programme',
        'ebook': 'Ebook',
        'complement': 'Complément alimentaire'
    }
    type_label = type_labels.get(item_type, 'Produit')

    subject = f"Confirmation d'achat - {item_name}"

    text_body = f"""
Salut {user.prenom}!

Merci pour ton achat! 🎉

Tu viens d'acheter: {item_name}
Type: {type_label}
Prix: {item.prix}€

"""

    if item_type == 'programme':
        text_body += f"""
Tu peux maintenant accéder à ton programme depuis ton tableau de bord:
https://fitgang.fr/dashboard

"""
    elif item_type == 'ebook':
        text_body += f"""
Tu peux télécharger ton ebook depuis ton tableau de bord:
https://fitgang.fr/dashboard

"""
    elif item_type == 'complement':
        text_body += f"""
Tu trouveras le lien d'achat sur la page du produit:
https://fitgang.fr/complement/{item.id}

"""

    text_body += """
N'hésite pas à nous contacter si tu as des questions!

À très vite,
L'équipe FitGang
"""

    html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #28a745; border-bottom: 3px solid #28a745; padding-bottom: 10px;">
            Merci pour ton achat! 🎉
        </h1>

        <p>Salut <strong>{user.prenom}</strong>!</p>

        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #dc3545;">Détails de ton achat</h3>
            <p><strong>{item_name}</strong></p>
            <p style="color: #666;">Type: {type_label}</p>
            <p style="font-size: 24px; color: #28a745; margin: 10px 0;"><strong>{item.prix}€</strong></p>
        </div>

"""

    if item_type == 'programme':
        html_body += f"""
        <p style="margin-top: 30px;">
            <a href="https://fitgang.fr/dashboard"
               style="background-color: #dc3545; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                Accéder à mon programme
            </a>
        </p>
"""
    elif item_type == 'ebook':
        html_body += f"""
        <p style="margin-top: 30px;">
            <a href="https://fitgang.fr/dashboard"
               style="background-color: #dc3545; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                Télécharger mon ebook
            </a>
        </p>
"""
    elif item_type == 'complement':
        html_body += f"""
        <p style="margin-top: 30px;">
            <a href="https://fitgang.fr/complement/{item.id}"
               style="background-color: #dc3545; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                Voir le lien d'achat
            </a>
        </p>
"""

    html_body += """
        <p style="margin-top: 30px; color: #666; font-size: 14px;">
            N'hésite pas à nous contacter si tu as des questions!<br>
            À très vite,<br>
            <strong>L'équipe FitGang</strong>
        </p>
    </div>
</body>
</html>
"""

    return send_email(subject, user.email, text_body, html_body)


def send_admin_notification_email(admin_email, user, item, item_type):
    """
    Envoie un email de notification à l'admin lors d'un nouvel achat
    """
    # Déterminer le nom du produit
    item_name = getattr(item, 'titre', None) or getattr(item, 'nom', 'Produit')

    type_labels = {
        'programme': 'Programme',
        'ebook': 'Ebook',
        'complement': 'Complément'
    }
    type_label = type_labels.get(item_type, 'Produit')

    subject = f"🔔 Nouvel achat: {item_name}"

    text_body = f"""
Nouvel achat sur FitGang!

Client: {user.prenom} {user.nom} ({user.email})
Produit: {item_name}
Type: {type_label}
Prix: {item.prix}€

Accède au dashboard admin:
https://fitgang.fr/admin/dashboard
"""

    html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #28a745; border-bottom: 3px solid #28a745; padding-bottom: 10px;">
            🔔 Nouvel achat sur FitGang!
        </h1>

        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #dc3545;">Détails de l'achat</h3>
            <p><strong>Client:</strong> {user.prenom} {user.nom}</p>
            <p><strong>Email:</strong> {user.email}</p>
            <p><strong>Produit:</strong> {item_name}</p>
            <p><strong>Type:</strong> {type_label}</p>
            <p style="font-size: 24px; color: #28a745; margin: 10px 0;"><strong>{item.prix}€</strong></p>
        </div>

        <p style="margin-top: 30px;">
            <a href="https://fitgang.fr/admin/dashboard"
               style="background-color: #dc3545; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                Accéder au dashboard admin
            </a>
        </p>
    </div>
</body>
</html>
"""

    return send_email(subject, admin_email, text_body, html_body)
