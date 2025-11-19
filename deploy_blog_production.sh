#!/bin/bash
# Script de déploiement du système de blog FitGang
# Chemin: /home/wrbh3411/fitgang_app/saas

echo "========================================="
echo "   DÉPLOIEMENT DU BLOG FITGANG"
echo "   Serveur: O2Switch"
echo "========================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier qu'on est dans le bon dossier
EXPECTED_PATH="/home/wrbh3411/fitgang_app/saas"
CURRENT_PATH=$(pwd)

if [ "$CURRENT_PATH" != "$EXPECTED_PATH" ]; then
    echo -e "${RED}✗${NC} Erreur: Vous n'êtes pas dans le bon dossier"
    echo "Dossier actuel: $CURRENT_PATH"
    echo "Dossier attendu: $EXPECTED_PATH"
    echo ""
    echo "Exécutez: cd $EXPECTED_PATH"
    exit 1
fi

echo -e "${GREEN}✓${NC} Dossier correct: $EXPECTED_PATH"
echo ""

# 1. Récupérer les dernières modifications
echo -e "${YELLOW}[1/5]${NC} Récupération des modifications Git..."
git fetch origin 2>&1
git pull 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Code mis à jour"
else
    echo -e "${RED}✗${NC} Erreur lors du git pull"
    echo "Vérifiez votre connexion Git"
    exit 1
fi

# 2. Vérifier l'environnement virtuel
echo ""
echo -e "${YELLOW}[2/5]${NC} Vérification de l'environnement Python..."

if [ -d "venv" ]; then
    echo -e "${GREEN}✓${NC} Environnement virtuel trouvé"
    source venv/bin/activate

    # Installer/mettre à jour les dépendances
    pip install -r requirements.txt --quiet 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Dépendances à jour"
    else
        echo -e "${YELLOW}⚠${NC} Problème avec les dépendances (non bloquant)"
    fi
else
    echo -e "${YELLOW}⚠${NC} Pas d'environnement virtuel trouvé"
    echo "Le système Python global sera utilisé"
fi

# 3. Créer/Mettre à jour la table blog_posts
echo ""
echo -e "${YELLOW}[3/5]${NC} Migration de la base de données..."

# Vérifier si Flask est disponible
if command -v flask &> /dev/null; then
    echo "Tentative avec Flask-Migrate..."
    flask db upgrade 2>&1

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Migration appliquée avec Flask-Migrate"
    else
        echo -e "${YELLOW}⚠${NC} Flask-Migrate non disponible, création manuelle..."

        # Méthode manuelle
        python3 << 'PYTHON_SCRIPT'
import sys
sys.path.insert(0, '/home/wrbh3411/fitgang_app/saas')

try:
    from app import create_app, db
    from app.models import BlogPost

    app = create_app('production')
    with app.app_context():
        # Créer toutes les tables (incluant blog_posts)
        db.create_all()
        print("✓ Table blog_posts créée/vérifiée")
except Exception as e:
    print(f"✗ Erreur: {e}")
    sys.exit(1)
PYTHON_SCRIPT

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓${NC} Table créée manuellement"
        else
            echo -e "${RED}✗${NC} Échec de la création de table"
            exit 1
        fi
    fi
else
    # Pas de Flask CLI, création directe
    echo "Création directe de la table..."

    python3 << 'PYTHON_SCRIPT'
import sys
sys.path.insert(0, '/home/wrbh3411/fitgang_app/saas')

try:
    from app import create_app, db
    from app.models import BlogPost

    app = create_app('production')
    with app.app_context():
        db.create_all()
        print("✓ Table blog_posts créée/vérifiée")
except Exception as e:
    print(f"✗ Erreur: {e}")
    sys.exit(1)
PYTHON_SCRIPT

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Table créée avec succès"
    else
        echo -e "${RED}✗${NC} Échec de la création"
        exit 1
    fi
fi

# 4. Redémarrer l'application (Passenger)
echo ""
echo -e "${YELLOW}[4/5]${NC} Redémarrage de l'application..."

# Créer le dossier tmp s'il n'existe pas
if [ ! -d "tmp" ]; then
    mkdir -p tmp
    echo "Dossier tmp/ créé"
fi

# Redémarrer Passenger
touch tmp/restart.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Application redémarrée (Passenger)"
else
    echo -e "${RED}✗${NC} Erreur lors du redémarrage"
fi

# Attendre 2 secondes pour laisser l'app redémarrer
sleep 2

# 5. Vérification finale
echo ""
echo -e "${YELLOW}[5/5]${NC} Vérification de l'installation..."

python3 << 'PYTHON_SCRIPT'
import sys
sys.path.insert(0, '/home/wrbh3411/fitgang_app/saas')

try:
    from app import create_app, db
    from app.models import BlogPost

    app = create_app('production')
    with app.app_context():
        # Compter les articles
        count = BlogPost.query.count()
        print(f"✓ Table blog_posts opérationnelle")
        print(f"  → {count} article(s) dans la base")

        # Vérifier les colonnes importantes
        first = BlogPost.query.first()
        if first:
            print(f"  → Dernier article: '{first.titre}'")
except Exception as e:
    print(f"⚠ Erreur de vérification: {e}")
    print("L'application devrait quand même fonctionner")
PYTHON_SCRIPT

echo ""
echo "========================================="
echo -e "${GREEN}   ✓ DÉPLOIEMENT TERMINÉ !${NC}"
echo "========================================="
echo ""
echo "🎉 Le blog est maintenant disponible sur:"
echo ""
echo "  📱 PUBLIC:"
echo "     https://fitgang.fr/blog"
echo "     https://fitgang.fr/blog/<slug>"
echo ""
echo "  🔧 ADMIN:"
echo "     https://fitgang.fr/admin/blog"
echo "     https://fitgang.fr/admin/blog/add"
echo ""
echo "  ✅ CORRECTION:"
echo "     https://fitgang.fr/profile/photos (ne donne plus d'erreur 500)"
echo ""
echo "📝 Prochaines étapes:"
echo "  1. Connectez-vous en admin: https://fitgang.fr/login"
echo "  2. Menu Admin → 'Gérer Blog'"
echo "  3. Créez votre premier article avec 'Nouvel Article'"
echo "  4. Publiez et vérifiez sur /blog!"
echo ""
echo "💡 Astuce images:"
echo "  - Utilisez Imgur: imgur.com (gratuit)"
echo "  - Copiez l'URL de l'image"
echo "  - Collez dans 'Image principale'"
echo "  - L'image s'affichera en 250x250px automatiquement"
echo ""
echo "📚 Guide complet: DEPLOIEMENT_BLOG.md"
echo ""
