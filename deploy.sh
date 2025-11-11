#!/bin/bash
# Script de déploiement automatique pour FitGang
# À exécuter sur le serveur de production

set -e  # Arrêter en cas d'erreur

echo "=========================================="
echo "DÉPLOIEMENT FITGANG"
echo "=========================================="

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BRANCH="claude/fix-email-campaigns-011CV29exAWnnTfzcJ4vZoRk"
APP_DIR="/var/www/fitgang"

echo -e "\n${YELLOW}1. Vérification du répertoire...${NC}"
if [ ! -d "$APP_DIR" ]; then
    echo -e "${RED}✗ Le répertoire $APP_DIR n'existe pas!${NC}"
    exit 1
fi
cd "$APP_DIR"
echo -e "${GREEN}✓ Répertoire OK${NC}"

echo -e "\n${YELLOW}2. Sauvegarde de l'état actuel...${NC}"
git stash || echo "Rien à sauvegarder"
echo -e "${GREEN}✓ Sauvegarde effectuée${NC}"

echo -e "\n${YELLOW}3. Récupération des modifications...${NC}"
git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"
echo -e "${GREEN}✓ Code mis à jour${NC}"

echo -e "\n${YELLOW}4. Vérification des fichiers critiques...${NC}"

# Vérifier que HomepageProgrammesForm existe dans forms.py
if grep -q "class HomepageProgrammesForm" app/forms.py; then
    echo -e "${GREEN}✓ app/forms.py contient HomepageProgrammesForm${NC}"
else
    echo -e "${RED}✗ HomepageProgrammesForm manquant dans forms.py${NC}"
    exit 1
fi

# Vérifier que le template existe
if [ -f "app/templates/admin_homepage_programmes.html" ]; then
    echo -e "${GREEN}✓ Template admin_homepage_programmes.html présent${NC}"
else
    echo -e "${RED}✗ Template admin_homepage_programmes.html manquant${NC}"
    exit 1
fi

# Vérifier que la route existe dans routes.py
if grep -q "def admin_homepage_programmes" app/routes.py; then
    echo -e "${GREEN}✓ Route admin_homepage_programmes présente${NC}"
else
    echo -e "${RED}✗ Route admin_homepage_programmes manquante${NC}"
    exit 1
fi

echo -e "\n${YELLOW}5. Redémarrage de l'application...${NC}"
sudo systemctl restart fitgang
sleep 2
echo -e "${GREEN}✓ Application redémarrée${NC}"

echo -e "\n${YELLOW}6. Vérification du statut...${NC}"
if sudo systemctl is-active --quiet fitgang; then
    echo -e "${GREEN}✓ Le service fitgang est actif${NC}"
else
    echo -e "${RED}✗ Le service fitgang n'est PAS actif!${NC}"
    echo -e "\n${YELLOW}Logs du service:${NC}"
    sudo journalctl -u fitgang -n 20 --no-pager
    exit 1
fi

echo -e "\n${YELLOW}7. Derniers logs (20 lignes):${NC}"
sudo journalctl -u fitgang -n 20 --no-pager

echo -e "\n=========================================="
echo -e "${GREEN}✓ DÉPLOIEMENT TERMINÉ AVEC SUCCÈS!${NC}"
echo "=========================================="
echo ""
echo "Tu peux maintenant:"
echo "  - Accéder au dashboard: https://fitgang.fr/admin"
echo "  - Modifier les programmes: https://fitgang.fr/admin/homepage-programmes"
echo ""
