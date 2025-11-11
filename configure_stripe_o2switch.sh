#!/bin/bash
# Script de configuration Stripe simplifié pour o2switch
# Sans sudo, adapté pour hébergement mutualisé

echo "=========================================="
echo "   CONFIGURATION STRIPE - o2switch"
echo "=========================================="
echo ""

# Vérifier qu'on est dans le bon répertoire
if [ ! -f "config.py" ]; then
    echo "✗ Erreur: Execute ce script depuis /home/wrbh3411/fitgang.fr"
    exit 1
fi

echo "Étape 1: Créer/Éditer le fichier .env"
echo "--------------------------------------"
echo ""
echo "1. Va sur https://dashboard.stripe.com"
echo "2. Assure-toi d'être en mode TEST (toggle en haut à droite)"
echo "3. Va dans: Developers > API keys"
echo "4. Copie tes clés:"
echo "   - Publishable key (commence par pk_test_)"
echo "   - Secret key (clique sur 'Reveal', commence par sk_test_)"
echo ""
read -p "Appuie sur ENTER quand tu es prêt..."

echo ""
echo "Colle ta PUBLISHABLE KEY (pk_test_...):"
read PUBLIC_KEY

echo ""
echo "Colle ta SECRET KEY (sk_test_...):"
read SECRET_KEY

# Vérifier le format
if [[ ! "$PUBLIC_KEY" =~ ^pk_test_ ]]; then
    echo "⚠️  Attention: La clé publique devrait commencer par pk_test_"
    read -p "Continuer quand même? (y/n): " CONTINUE
    if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

if [[ ! "$SECRET_KEY" =~ ^sk_test_ ]]; then
    echo "⚠️  Attention: La clé secrète devrait commencer par sk_test_"
    read -p "Continuer quand même? (y/n): " CONTINUE
    if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Créer ou mettre à jour .env
if [ ! -f ".env" ]; then
    echo "Création du fichier .env..."
    touch .env
fi

# Supprimer les anciennes lignes Stripe
sed -i '/^STRIPE_PUBLIC_KEY=/d' .env 2>/dev/null || true
sed -i '/^STRIPE_SECRET_KEY=/d' .env 2>/dev/null || true

# Ajouter les nouvelles clés
echo "" >> .env
echo "# Configuration Stripe - Mode TEST" >> .env
echo "STRIPE_PUBLIC_KEY=$PUBLIC_KEY" >> .env
echo "STRIPE_SECRET_KEY=$SECRET_KEY" >> .env

echo ""
echo "✓ Clés Stripe sauvegardées dans .env"
echo ""

# Redémarrer l'application
echo "Redémarrage de l'application..."
mkdir -p tmp
touch tmp/restart.txt
echo "✓ Application redémarrée"
echo ""

echo "=========================================="
echo "   CONFIGURATION TERMINÉE!"
echo "=========================================="
echo ""
echo "Pour tester:"
echo "1. Va sur https://fitgang.fr"
echo "2. Connecte-toi et achète un programme"
echo "3. Utilise la carte de test: 4242 4242 4242 4242"
echo "4. Date: 12/34, CVC: 123"
echo ""
echo "Vérifie ensuite sur:"
echo "https://dashboard.stripe.com/test/payments"
echo ""
