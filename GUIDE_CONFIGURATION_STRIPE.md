# Guide de Configuration Stripe pour FitGang

## Vue d'ensemble

FitGang utilise Stripe pour gérer les paiements des programmes, ebooks et compléments alimentaires.

## Étape 1: Créer un compte Stripe

1. Va sur https://stripe.com
2. Clique sur "S'inscrire" ou "Sign up"
3. Crée ton compte professionnel
4. Vérifie ton email

## Étape 2: Récupérer tes clés API

### En mode TEST (pour développement)

1. Connecte-toi à https://dashboard.stripe.com
2. Assure-toi que le toggle est sur **"Test mode"** (en haut à droite)
3. Va dans **Developers > API keys**
4. Tu verras:
   - **Publishable key** (commence par `pk_test_...`)
   - **Secret key** (commence par `sk_test_...`) - clique sur "Reveal" pour la voir

### En mode LIVE (pour production)

⚠️ **ATTENTION**: Ne passe en mode LIVE qu'après avoir testé en mode TEST!

1. Dans le dashboard Stripe, bascule sur **"Live mode"**
2. Va dans **Developers > API keys**
3. Tu verras:
   - **Publishable key** (commence par `pk_live_...`)
   - **Secret key** (commence par `sk_live_...`)

## Étape 3: Configurer les clés dans FitGang

### Sur ton serveur de production

1. Connecte-toi en SSH à ton serveur
2. Édite le fichier `.env`:
   ```bash
   cd /var/www/fitgang
   nano .env
   ```

3. Ajoute ou modifie ces lignes:
   ```bash
   # Pour le mode TEST
   STRIPE_PUBLIC_KEY=pk_test_VOTRE_CLE_PUBLIQUE_ICI
   STRIPE_SECRET_KEY=sk_test_VOTRE_CLE_SECRETE_ICI

   # Pour le mode LIVE (une fois testé)
   # STRIPE_PUBLIC_KEY=pk_live_VOTRE_CLE_PUBLIQUE_ICI
   # STRIPE_SECRET_KEY=sk_live_VOTRE_CLE_SECRETE_ICI
   ```

4. Sauvegarde le fichier (Ctrl+O, Enter, Ctrl+X)

5. Redémarre l'application:
   ```bash
   sudo systemctl restart fitgang
   ```

## Étape 4: Configurer les webhooks (optionnel mais recommandé)

Les webhooks permettent à Stripe de notifier ton application en temps réel des événements de paiement.

### Configuration du webhook

1. Va dans le dashboard Stripe: **Developers > Webhooks**
2. Clique sur **"Add endpoint"**
3. Entre l'URL du webhook:
   ```
   https://fitgang.fr/webhook/stripe
   ```
4. Sélectionne les événements à écouter:
   - `checkout.session.completed`
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`

5. Clique sur **"Add endpoint"**

6. Copie le **Signing secret** (commence par `whsec_...`)

7. Ajoute-le dans ton `.env`:
   ```bash
   STRIPE_WEBHOOK_SECRET=whsec_VOTRE_SECRET_ICI
   ```

8. Redémarre l'application:
   ```bash
   sudo systemctl restart fitgang
   ```

## Étape 5: Tester les paiements

### En mode TEST

Stripe fournit des numéros de carte de test:

#### Paiement réussi:
- **Numéro**: 4242 4242 4242 4242
- **Date d'expiration**: N'importe quelle date future (ex: 12/34)
- **CVC**: N'importe quel 3 chiffres (ex: 123)

#### Paiement refusé:
- **Numéro**: 4000 0000 0000 0002

#### Authentification 3D Secure:
- **Numéro**: 4000 0027 6000 3184

### Test complet

1. Va sur https://fitgang.fr
2. Connecte-toi avec un compte utilisateur
3. Va sur la page **Programmes** ou **Ebooks**
4. Clique sur **"Acheter"** sur un produit
5. Tu seras redirigé vers Stripe Checkout
6. Utilise une carte de test (4242 4242 4242 4242)
7. Complète le paiement
8. Tu devrais être redirigé vers ton dashboard avec un message de succès
9. Le produit devrait apparaître dans ta bibliothèque

### Vérifier dans le dashboard Stripe

1. Va dans **Payments** dans le dashboard Stripe
2. Tu verras le paiement test
3. Vérifie que le montant et les détails sont corrects

## Étape 6: Passer en production (LIVE)

⚠️ **Avant de passer en LIVE**:

1. **Vérifie ton compte Stripe**:
   - Fournis toutes les informations demandées (identité, coordonnées bancaires, etc.)
   - Complète la vérification d'identité si nécessaire

2. **Teste TOUT en mode TEST**:
   - Achats de programmes
   - Achats d'ebooks
   - Achats de compléments
   - Annulation de paiement
   - Emails de confirmation

3. **Configure les webhooks en LIVE**:
   - Répète l'étape 4 mais en mode LIVE
   - Utilise une URL webhook LIVE

4. **Remplace les clés dans `.env`**:
   ```bash
   # Commente les clés TEST
   # STRIPE_PUBLIC_KEY=pk_test_...
   # STRIPE_SECRET_KEY=sk_test_...

   # Active les clés LIVE
   STRIPE_PUBLIC_KEY=pk_live_VOTRE_CLE_LIVE
   STRIPE_SECRET_KEY=sk_live_VOTRE_CLE_LIVE
   STRIPE_WEBHOOK_SECRET=whsec_VOTRE_SECRET_LIVE
   ```

5. **Redémarre l'application**:
   ```bash
   sudo systemctl restart fitgang
   ```

## Configuration actuelle dans le code

### Fichiers concernés

1. **config.py** (lignes 26-29):
   ```python
   STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY') or 'pk_test_your_key_here'
   STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') or 'sk_test_your_key_here'
   STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET') or 'whsec_your_webhook_secret'
   ```

2. **app/routes.py** (ligne 25):
   ```python
   stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_your_key_here')
   ```

3. **Routes de paiement**:
   - `/checkout/<item_type>/<item_id>` - Créer une session de paiement
   - `/checkout/success` - Gérer le succès du paiement
   - `/checkout/cancel` - Gérer l'annulation

## Fonctionnalités actuelles

### Ce qui fonctionne:
✅ Paiement de programmes
✅ Paiement d'ebooks
✅ Paiement de compléments
✅ Redirection après paiement réussi
✅ Redirection après annulation
✅ Enregistrement des achats en base de données
✅ Emails de confirmation (client + admin)
✅ Détection des achats en double

### À améliorer (optionnel):
⏳ Route webhook pour gérer les événements Stripe
⏳ Gestion des remboursements
⏳ Historique des paiements échoués
⏳ Codes promo / réductions

## Vérifier que tout fonctionne

### Commandes de vérification

```bash
# Vérifier que les variables sont bien chargées
cd /var/www/fitgang
python3 -c "from config import Config; print('Public key:', Config.STRIPE_PUBLIC_KEY[:20] + '...'); print('Secret key:', Config.STRIPE_SECRET_KEY[:20] + '...')"

# Vérifier les logs de l'application
sudo journalctl -u fitgang -n 50 --no-pager | grep -i stripe

# Tester une connexion à l'API Stripe
python3 -c "import stripe; import os; stripe.api_key = os.getenv('STRIPE_SECRET_KEY'); print('✓ Connexion Stripe OK' if stripe.api_key else '✗ Clé Stripe manquante')"
```

## Sécurité

⚠️ **IMPORTANT**:

1. **Ne commite JAMAIS tes clés dans Git**:
   - Les clés doivent rester dans `.env` uniquement
   - `.env` doit être dans `.gitignore`

2. **Protège ton fichier `.env`**:
   ```bash
   chmod 600 /var/www/fitgang/.env
   ```

3. **Utilise toujours HTTPS en production**:
   - Stripe refuse les webhooks en HTTP
   - Les clés LIVE ne fonctionnent qu'en HTTPS

4. **Renouvelle tes clés régulièrement**:
   - Tu peux générer de nouvelles clés dans le dashboard Stripe
   - Les anciennes continuent de fonctionner (roll secret)

## Tarification Stripe

### Frais par transaction:
- **En Europe**: 1.4% + 0.25€ par transaction réussie
- **Cartes européennes**: 1.4% + 0.25€
- **Cartes internationales**: 2.9% + 0.25€

### Exemple:
- Programme à 29€
- Frais Stripe: (29 × 1.4%) + 0.25€ = 0.41€ + 0.25€ = **0.66€**
- Tu reçois: **28.34€**

## Support

- **Documentation Stripe**: https://stripe.com/docs
- **Dashboard Stripe**: https://dashboard.stripe.com
- **Support Stripe**: https://support.stripe.com

## Besoin d'aide?

Si tu as des questions ou des problèmes:
1. Vérifie les logs: `sudo journalctl -u fitgang -n 100`
2. Consulte les événements Stripe dans le dashboard
3. Teste avec les cartes de test en mode TEST
