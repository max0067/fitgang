#!/bin/bash
# Script de déploiement du système de blog FitGang

echo "========================================="
echo "   DÉPLOIEMENT DU BLOG FITGANG"
echo "========================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Récupérer les dernières modifications
echo -e "${YELLOW}[1/5]${NC} Récupération des modifications..."
git fetch origin
git pull origin claude/fix-blog-layout-cache-01BREgfFyut2YeX3GdQanxWK
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Modifications récupérées"
else
    echo -e "${RED}✗${NC} Erreur lors du pull"
    echo "Essayez: git pull"
    exit 1
fi

# 2. Installer les dépendances (si nouvelles)
echo ""
echo -e "${YELLOW}[2/5]${NC} Vérification des dépendances..."
if [ -d "venv" ]; then
    source venv/bin/activate
    pip install -r requirements.txt --quiet
    echo -e "${GREEN}✓${NC} Dépendances à jour"
else
    echo -e "${RED}✗${NC} Environnement virtuel non trouvé"
    echo "Créez-le avec: python3 -m venv venv"
fi

# 3. Appliquer les migrations de base de données
echo ""
echo -e "${YELLOW}[3/5]${NC} Migration de la base de données..."

# Vérifier si Flask-Migrate est configuré
if [ -d "migrations" ]; then
    # Méthode 1: Avec Flask-Migrate
    echo "Utilisation de Flask-Migrate..."
    flask db upgrade
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Migration appliquée avec Flask-Migrate"
    else
        echo -e "${YELLOW}⚠${NC} Flask-Migrate échoué, tentative de création manuelle..."
        python3 << 'PYTHON_SCRIPT'
from app import create_app, db
from app.models import BlogPost

app = create_app('production')
with app.app_context():
    try:
        # Créer la table si elle n'existe pas
        db.create_all()
        print("✓ Table blog_posts créée")
    except Exception as e:
        print(f"Erreur: {e}")
PYTHON_SCRIPT
    fi
else
    # Méthode 2: Création manuelle de la table
    echo "Création manuelle de la table blog_posts..."
    python3 << 'PYTHON_SCRIPT'
from app import create_app, db
from app.models import BlogPost

app = create_app('production')
with app.app_context():
    try:
        # Créer la table si elle n'existe pas
        db.create_all()
        print("✓ Table blog_posts créée")
    except Exception as e:
        print(f"Erreur: {e}")
PYTHON_SCRIPT
fi

# 4. Redémarrer l'application
echo ""
echo -e "${YELLOW}[4/5]${NC} Redémarrage de l'application..."

# Pour o2switch/Hostinger avec Passenger
if [ -f "tmp/restart.txt" ]; then
    touch tmp/restart.txt
    echo -e "${GREEN}✓${NC} Application redémarrée (Passenger)"
else
    mkdir -p tmp
    touch tmp/restart.txt
    echo -e "${GREEN}✓${NC} Application redémarrée (Passenger - nouveau)"
fi

# 5. Vérification
echo ""
echo -e "${YELLOW}[5/5]${NC} Vérification..."
python3 << 'PYTHON_SCRIPT'
from app import create_app, db
from app.models import BlogPost

app = create_app('production')
with app.app_context():
    try:
        # Vérifier que la table existe
        count = BlogPost.query.count()
        print(f"✓ Table blog_posts OK ({count} articles)")
    except Exception as e:
        print(f"⚠ Erreur de vérification: {e}")
PYTHON_SCRIPT

echo ""
echo "========================================="
echo -e "${GREEN}   DÉPLOIEMENT TERMINÉ !${NC}"
echo "========================================="
echo ""
echo "Prochaines étapes:"
echo "1. Accédez à https://fitgang.fr/blog pour voir le blog"
echo "2. Connectez-vous en admin et allez dans Admin > Gérer Blog"
echo "3. Créez votre premier article de blog!"
echo ""
echo "Routes disponibles:"
echo "  - /blog                    : Liste des articles"
echo "  - /blog/<slug>            : Article détaillé"
echo "  - /admin/blog             : Gestion admin"
echo "  - /admin/blog/add         : Créer un article"
echo ""
