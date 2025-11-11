#!/bin/bash
# Script interactif de configuration Stripe pour FitGang

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================="
echo "   CONFIGURATION STRIPE POUR FITGANG"
echo -e "==========================================${NC}\n"

# Vérifier qu'on est dans le bon répertoire
if [ ! -f "config.py" ]; then
    echo -e "${RED}✗ Erreur: Ce script doit être exécuté depuis le répertoire racine de FitGang${NC}"
    exit 1
fi

# Vérifier si .env existe
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Le fichier .env n'existe pas. Création...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Fichier .env créé depuis .env.example${NC}"
    else
        touch .env
        echo -e "${GREEN}✓ Fichier .env créé${NC}"
    fi
fi

echo -e "${YELLOW}Choisis le mode Stripe:${NC}"
echo "1) Mode TEST (pour développement et tests)"
echo "2) Mode LIVE (pour production - nécessite un compte vérifié)"
echo ""
read -p "Ton choix (1 ou 2): " MODE_CHOICE

if [ "$MODE_CHOICE" == "1" ]; then
    MODE="TEST"
    echo -e "\n${BLUE}Mode TEST sélectionné${NC}"
    echo -e "${YELLOW}Tu peux trouver tes clés TEST sur:${NC}"
    echo "https://dashboard.stripe.com/test/apikeys"
else
    MODE="LIVE"
    echo -e "\n${BLUE}Mode LIVE sélectionné${NC}"
    echo -e "${RED}⚠️  ATTENTION: Assure-toi d'avoir:${NC}"
    echo "   - Vérifié ton compte Stripe"
    echo "   - Testé en mode TEST avant"
    echo "   - Configuré HTTPS sur ton site"
    echo ""
    echo -e "${YELLOW}Tu peux trouver tes clés LIVE sur:${NC}"
    echo "https://dashboard.stripe.com/apikeys"
fi

echo ""
echo -e "${YELLOW}📋 Ouvre le lien ci-dessus dans ton navigateur pour copier tes clés${NC}"
echo ""
read -p "Appuie sur ENTER quand tu es prêt à continuer..."

# Demander la clé publique
echo ""
echo -e "${BLUE}1. Clé publique (Publishable key)${NC}"
if [ "$MODE" == "TEST" ]; then
    echo -e "Elle commence par ${GREEN}pk_test_${NC}"
else
    echo -e "Elle commence par ${GREEN}pk_live_${NC}"
fi
read -p "Colle ta clé publique: " PUBLIC_KEY

# Vérifier le format
if [ "$MODE" == "TEST" ] && [[ ! "$PUBLIC_KEY" =~ ^pk_test_ ]]; then
    echo -e "${RED}✗ Erreur: La clé publique TEST doit commencer par pk_test_${NC}"
    exit 1
elif [ "$MODE" == "LIVE" ] && [[ ! "$PUBLIC_KEY" =~ ^pk_live_ ]]; then
    echo -e "${RED}✗ Erreur: La clé publique LIVE doit commencer par pk_live_${NC}"
    exit 1
fi

# Demander la clé secrète
echo ""
echo -e "${BLUE}2. Clé secrète (Secret key)${NC}"
if [ "$MODE" == "TEST" ]; then
    echo -e "Elle commence par ${GREEN}sk_test_${NC}"
else
    echo -e "Elle commence par ${GREEN}sk_live_${NC}"
fi
echo -e "${YELLOW}⚠️  Dans le dashboard Stripe, clique sur 'Reveal' pour voir la clé${NC}"
read -p "Colle ta clé secrète: " SECRET_KEY

# Vérifier le format
if [ "$MODE" == "TEST" ] && [[ ! "$SECRET_KEY" =~ ^sk_test_ ]]; then
    echo -e "${RED}✗ Erreur: La clé secrète TEST doit commencer par sk_test_${NC}"
    exit 1
elif [ "$MODE" == "LIVE" ] && [[ ! "$SECRET_KEY" =~ ^sk_live_ ]]; then
    echo -e "${RED}✗ Erreur: La clé secrète LIVE doit commencer par sk_live_${NC}"
    exit 1
fi

# Demander si on configure le webhook
echo ""
echo -e "${BLUE}3. Configuration du webhook (optionnel mais recommandé)${NC}"
read -p "Veux-tu configurer un webhook maintenant? (y/n): " WEBHOOK_CHOICE

if [[ "$WEBHOOK_CHOICE" =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${YELLOW}Pour configurer le webhook:${NC}"
    echo "1. Va sur: https://dashboard.stripe.com/webhooks"
    if [ "$MODE" == "LIVE" ]; then
        echo "   (Assure-toi d'être en mode LIVE)"
    else
        echo "   (Assure-toi d'être en mode TEST)"
    fi
    echo "2. Clique sur 'Add endpoint'"
    echo "3. Entre l'URL: https://fitgang.fr/webhook/stripe"
    echo "4. Sélectionne les événements:"
    echo "   - checkout.session.completed"
    echo "   - payment_intent.succeeded"
    echo "   - payment_intent.payment_failed"
    echo "5. Clique sur 'Add endpoint'"
    echo "6. Copie le 'Signing secret' (commence par whsec_)"
    echo ""
    read -p "Colle le signing secret du webhook: " WEBHOOK_SECRET

    if [[ ! "$WEBHOOK_SECRET" =~ ^whsec_ ]]; then
        echo -e "${YELLOW}⚠️  Le secret webhook devrait commencer par whsec_${NC}"
        echo -e "${YELLOW}   Je vais quand même l'enregistrer${NC}"
    fi
else
    WEBHOOK_SECRET=""
fi

# Sauvegarder dans .env
echo ""
echo -e "${YELLOW}Sauvegarde des clés dans .env...${NC}"

# Supprimer les anciennes clés Stripe si elles existent
sed -i '/^STRIPE_PUBLIC_KEY=/d' .env
sed -i '/^STRIPE_SECRET_KEY=/d' .env
sed -i '/^STRIPE_WEBHOOK_SECRET=/d' .env

# Ajouter les nouvelles clés
echo "" >> .env
echo "# Configuration Stripe - Mode $MODE" >> .env
echo "STRIPE_PUBLIC_KEY=$PUBLIC_KEY" >> .env
echo "STRIPE_SECRET_KEY=$SECRET_KEY" >> .env
if [ -n "$WEBHOOK_SECRET" ]; then
    echo "STRIPE_WEBHOOK_SECRET=$WEBHOOK_SECRET" >> .env
fi

echo -e "${GREEN}✓ Clés Stripe sauvegardées dans .env${NC}"

# Protéger le fichier .env
chmod 600 .env
echo -e "${GREEN}✓ Permissions du fichier .env sécurisées (600)${NC}"

# Résumé
echo ""
echo -e "${BLUE}=========================================="
echo "   CONFIGURATION TERMINÉE"
echo -e "==========================================${NC}"
echo ""
echo -e "${GREEN}✓ Mode: $MODE${NC}"
echo -e "${GREEN}✓ Clé publique: ${PUBLIC_KEY:0:20}...${NC}"
echo -e "${GREEN}✓ Clé secrète: ${SECRET_KEY:0:20}...${NC}"
if [ -n "$WEBHOOK_SECRET" ]; then
    echo -e "${GREEN}✓ Webhook: configuré${NC}"
fi

echo ""
echo -e "${YELLOW}Prochaines étapes:${NC}"
echo ""

if [ "$MODE" == "TEST" ]; then
    echo "1. Redémarre l'application:"
    echo "   ${BLUE}sudo systemctl restart fitgang${NC}"
    echo ""
    echo "2. Teste un paiement avec une carte de test:"
    echo "   ${GREEN}Numéro: 4242 4242 4242 4242${NC}"
    echo "   ${GREEN}Date: 12/34${NC}"
    echo "   ${GREEN}CVC: 123${NC}"
    echo ""
    echo "3. Vérifie dans le dashboard Stripe:"
    echo "   ${BLUE}https://dashboard.stripe.com/test/payments${NC}"
    echo ""
    echo "4. Une fois que tout fonctionne, lance ce script à nouveau"
    echo "   en mode LIVE pour passer en production"
else
    echo "1. Redémarre l'application:"
    echo "   ${BLUE}sudo systemctl restart fitgang${NC}"
    echo ""
    echo "2. ${RED}Teste ABSOLUMENT avec de vrais paiements${NC}"
    echo "   ${YELLOW}(commence par de petits montants)${NC}"
    echo ""
    echo "3. Vérifie dans le dashboard Stripe:"
    echo "   ${BLUE}https://dashboard.stripe.com/payments${NC}"
    echo ""
    echo "4. ${GREEN}Tu es prêt à accepter de vrais paiements! 🎉${NC}"
fi

echo ""
echo -e "${YELLOW}Documentation complète: GUIDE_CONFIGURATION_STRIPE.md${NC}"
echo ""
