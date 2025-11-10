#!/bin/bash
# Script de déploiement automatique pour Hostinger
# Usage: ./deploy_hostinger.sh

set -e  # Arrêter en cas d'erreur

echo "🚀 Déploiement de FitGang sur Hostinger"
echo "========================================"

# Variables à configurer
HOSTINGER_USER="ton-username"  # ⚠️ CHANGE MOI
HOSTINGER_HOST="srv1.hostinger.com"  # ⚠️ CHANGE MOI
HOSTINGER_PORT="65002"  # ⚠️ CHANGE MOI
HOSTINGER_PATH="~/public_html"

echo ""
echo "⚠️  CONFIGURATION REQUISE:"
echo "   - HOSTINGER_USER: $HOSTINGER_USER"
echo "   - HOSTINGER_HOST: $HOSTINGER_HOST"
echo "   - HOSTINGER_PORT: $HOSTINGER_PORT"
echo ""

read -p "Les informations ci-dessus sont-elles correctes? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "❌ Édite le fichier deploy_hostinger.sh avec tes vraies informations"
    exit 1
fi

# Étape 1: Commit des derniers changements
echo ""
echo "📝 Étape 1/6: Commit des changements locaux..."
git add -A
read -p "Message de commit: " COMMIT_MSG
git commit -m "$COMMIT_MSG" || echo "Aucun changement à committer"
git push

# Étape 2: Connexion et mise à jour du code
echo ""
echo "📦 Étape 2/6: Mise à jour du code sur Hostinger..."
ssh -p $HOSTINGER_PORT $HOSTINGER_USER@$HOSTINGER_HOST << 'EOF'
    cd ~/public_html

    # Pull les derniers changements
    if [ -d .git ]; then
        git pull
    else
        echo "⚠️  Pas de repo Git trouvé. Clone ton repo manuellement."
    fi
EOF

# Étape 3: Installation des dépendances
echo ""
echo "📚 Étape 3/6: Installation des dépendances..."
ssh -p $HOSTINGER_PORT $HOSTINGER_USER@$HOSTINGER_HOST << 'EOF'
    cd ~/public_html

    # Activer l'environnement virtuel
    source venv/bin/activate

    # Installer/Mettre à jour les dépendances
    pip install --upgrade pip
    pip install -r requirements.txt
EOF

# Étape 4: Migrations de base de données (si nécessaire)
echo ""
echo "🗄️  Étape 4/6: Vérification de la base de données..."
ssh -p $HOSTINGER_PORT $HOSTINGER_USER@$HOSTINGER_HOST << 'EOF'
    cd ~/public_html
    source venv/bin/activate

    # Créer la DB si elle n'existe pas
    if [ ! -f fitgang.db ]; then
        echo "Création de la base de données..."
        python create_admin.py
    fi
EOF

# Étape 5: Backup de la base de données
echo ""
echo "💾 Étape 5/6: Backup de la base de données..."
ssh -p $HOSTINGER_PORT $HOSTINGER_USER@$HOSTINGER_HOST << 'EOF'
    cd ~/public_html

    if [ -f fitgang.db ]; then
        BACKUP_NAME="backups/fitgang_$(date +%Y%m%d_%H%M%S).db"
        mkdir -p backups
        cp fitgang.db $BACKUP_NAME
        echo "✅ Backup créé: $BACKUP_NAME"

        # Garder seulement les 10 derniers backups
        cd backups
        ls -t fitgang_*.db | tail -n +11 | xargs -r rm
    fi
EOF

# Étape 6: Redémarrer l'application
echo ""
echo "🔄 Étape 6/6: Redémarrage de l'application..."
ssh -p $HOSTINGER_PORT $HOSTINGER_USER@$HOSTINGER_HOST << 'EOF'
    cd ~/public_html
    mkdir -p tmp
    touch tmp/restart.txt
    echo "✅ Application redémarrée"
EOF

echo ""
echo "✅ DÉPLOIEMENT TERMINÉ!"
echo "========================"
echo ""
echo "🌐 Vérifie ton site: https://fitgang.fr"
echo ""
echo "📊 Commandes utiles:"
echo "   - Voir les logs: ssh -p $HOSTINGER_PORT $HOSTINGER_USER@$HOSTINGER_HOST 'tail -f ~/logs/error.log'"
echo "   - Redémarrer: ssh -p $HOSTINGER_PORT $HOSTINGER_USER@$HOSTINGER_HOST 'touch ~/public_html/tmp/restart.txt'"
echo ""
