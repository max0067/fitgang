"""
Module d'envoi d'emails en masse pour FitGang
Gère l'envoi par batch pour éviter de surcharger le serveur SMTP
"""
import time
from datetime import datetime
from flask import current_app
from app import db
from app.models import Newsletter, EmailCampaign
from app.email import send_email


def send_test_email(recipient_email, subject, html_body, text_body=None):
    """
    Envoie un email de test à un destinataire unique
    """
    if not text_body:
        # Créer une version texte basique si non fournie
        text_body = html_body.replace('<br>', '\n').replace('<p>', '').replace('</p>', '\n')

    success = send_email(subject, recipient_email, text_body, html_body)
    return success


def send_bulk_emails(campaign_id, batch_size=50, delay_between_batches=5):
    """
    Envoie les emails d'une campagne en masse par batch

    Args:
        campaign_id: ID de la campagne d'email
        batch_size: Nombre d'emails par batch (défaut: 50)
        delay_between_batches: Délai en secondes entre chaque batch (défaut: 5)

    Returns:
        dict: Statistiques d'envoi {sent: int, errors: int, total: int}
    """
    campaign = EmailCampaign.query.get(campaign_id)
    if not campaign:
        return {'error': 'Campagne introuvable', 'sent': 0, 'errors': 0, 'total': 0}

    # Mettre à jour le statut
    campaign.statut = 'en_cours'
    campaign.date_envoi = datetime.utcnow()
    db.session.commit()

    # Récupérer tous les emails actifs de la newsletter
    all_subscribers = Newsletter.query.filter_by(actif=True).all()
    total_emails = len(all_subscribers)
    campaign.emails_total = total_emails
    db.session.commit()

    sent_count = 0
    error_count = 0

    # Version texte de l'email
    text_body = campaign.contenu_texte or campaign.contenu_html.replace('<br>', '\n')

    try:
        # Envoyer par batch
        for i in range(0, total_emails, batch_size):
            batch = all_subscribers[i:i + batch_size]

            for subscriber in batch:
                try:
                    success = send_email(
                        campaign.sujet,
                        subscriber.email,
                        text_body,
                        campaign.contenu_html
                    )

                    if success:
                        sent_count += 1
                    else:
                        error_count += 1

                except Exception as e:
                    print(f"Erreur lors de l'envoi à {subscriber.email}: {e}")
                    error_count += 1

                # Mettre à jour la progression tous les 10 emails
                if (sent_count + error_count) % 10 == 0:
                    campaign.emails_envoyes = sent_count
                    campaign.emails_erreurs = error_count
                    db.session.commit()

            # Délai entre les batches pour ne pas surcharger le serveur SMTP
            if i + batch_size < total_emails:
                time.sleep(delay_between_batches)

        # Mettre à jour le statut final
        campaign.statut = 'terminee'
        campaign.emails_envoyes = sent_count
        campaign.emails_erreurs = error_count
        campaign.date_fin_envoi = datetime.utcnow()
        db.session.commit()

    except Exception as e:
        campaign.statut = 'erreur'
        campaign.emails_envoyes = sent_count
        campaign.emails_erreurs = error_count
        db.session.commit()
        print(f"Erreur critique lors de l'envoi de la campagne: {e}")

    return {
        'sent': sent_count,
        'errors': error_count,
        'total': total_emails
    }


def preview_campaign_recipients(campaign_id, limit=10):
    """
    Retourne un aperçu des destinataires d'une campagne
    """
    subscribers = Newsletter.query.filter_by(actif=True).limit(limit).all()
    return [sub.email for sub in subscribers]


def get_campaign_stats(campaign_id):
    """
    Retourne les statistiques d'une campagne
    """
    campaign = EmailCampaign.query.get(campaign_id)
    if not campaign:
        return None

    return {
        'nom': campaign.nom,
        'sujet': campaign.sujet,
        'statut': campaign.statut,
        'total': campaign.emails_total,
        'envoyes': campaign.emails_envoyes,
        'erreurs': campaign.emails_erreurs,
        'taux_succes': (campaign.emails_envoyes / campaign.emails_total * 100) if campaign.emails_total > 0 else 0,
        'date_creation': campaign.date_creation,
        'date_envoi': campaign.date_envoi,
        'date_fin': campaign.date_fin_envoi
    }
