#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour tester l'envoi d'une campagne email et voir tous les logs
"""
import os
import sys

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv('.env')

print("=" * 60)
print("TEST ENVOI CAMPAGNE EMAIL")
print("=" * 60)

# Importer l'application
from app import create_app, db
from app.models import EmailCampaign, Newsletter
from app.email_bulk import send_bulk_emails

# Créer l'application
app = create_app('production')

with app.app_context():
    # Trouver une campagne brouillon
    campaign = EmailCampaign.query.filter_by(statut='brouillon').first()

    if not campaign:
        print("\n✗ Aucune campagne en brouillon trouvée!")
        print("\nCampagnes disponibles:")
        all_campaigns = EmailCampaign.query.all()
        for c in all_campaigns:
            print(f"  - ID {c.id}: {c.nom} (statut: {c.statut})")
        sys.exit(1)

    print(f"\n📧 Campagne trouvée:")
    print(f"   ID: {campaign.id}")
    print(f"   Nom: {campaign.nom}")
    print(f"   Sujet: {campaign.sujet}")
    print(f"   Statut: {campaign.statut}")

    # Compter les destinataires
    subscribers_count = Newsletter.query.filter_by(actif=True).count()
    print(f"\n👥 Destinataires actifs: {subscribers_count}")

    if subscribers_count == 0:
        print("\n✗ Aucun destinataire actif! Ajoutez des emails à la newsletter d'abord.")
        sys.exit(1)

    # Demander confirmation
    response = input(f"\n⚠️  Voulez-vous VRAIMENT envoyer la campagne à {subscribers_count} destinataires? (oui/non): ")

    if response.lower() != 'oui':
        print("\n❌ Envoi annulé.")
        sys.exit(0)

    print("\n" + "=" * 60)
    print("DÉBUT DE L'ENVOI")
    print("=" * 60 + "\n")

    # Lancer l'envoi avec des petits batches pour voir les logs
    stats = send_bulk_emails(
        campaign.id,
        batch_size=5,  # Petits batches pour voir chaque email
        delay_between_batches=1  # 1 seconde entre chaque batch
    )

    print("\n" + "=" * 60)
    print("RÉSULTAT FINAL")
    print("=" * 60)
    print(f"✓ Emails envoyés: {stats['sent']}")
    print(f"✗ Erreurs: {stats['errors']}")
    print(f"📊 Total: {stats['total']}")

    if stats['errors'] > 0:
        print(f"\n⚠️  {stats['errors']} email(s) n'ont pas pu être envoyés.")
        print("Vérifiez les logs ci-dessus pour plus de détails.")
    else:
        print("\n🎉 Tous les emails ont été envoyés avec succès!")
