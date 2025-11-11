#!/bin/bash
# Script de configuration automatique de l'environnement de test
# Usage: ./setup_test_environment.sh

echo "═══════════════════════════════════════════════════════════════"
echo "  Configuration Environnement de Test - test.fitgang.fr"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Variables
PROD_DIR="/home/wrbh3411/fitgang.fr"
TEST_DIR="/home/wrbh3411/test.fitgang.fr"
BACKUP_DIR="/home/wrbh3411/backups"

# Vérifier qu'on est bien sur le serveur
if [ ! -d "/home/wrbh3411" ]; then
    echo "❌ Erreur: Ce script doit être exécuté sur le serveur o2switch"
    exit 1
fi

# Créer le dossier de backups si nécessaire
mkdir -p "$BACKUP_DIR"

echo "1️⃣  Copie de l'environnement de production vers test..."
echo ""

# Vérifier si le dossier test existe déjà
if [ -d "$TEST_DIR" ]; then
    echo "⚠️  Le dossier test.fitgang.fr existe déjà"
    read -p "Voulez-vous le supprimer et recommencer? (y/N): " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        echo "   Backup de l'ancien test..."
        tar -czf "$BACKUP_DIR/test.fitgang.fr_backup_$(date +%Y%m%d_%H%M%S).tar.gz" -C /home/wrbh3411 test.fitgang.fr
        rm -rf "$TEST_DIR"
    else
        echo "❌ Installation annulée"
        exit 1
    fi
fi

# Copier les fichiers de production
echo "   Copie des fichiers..."
cp -r "$PROD_DIR" "$TEST_DIR"

echo "✅ Copie terminée"
echo ""

echo "2️⃣  Configuration de l'environnement de test..."
echo ""

# Supprimer la base de données de production (on va en créer une nouvelle)
if [ -f "$TEST_DIR/fitgang.db" ]; then
    echo "   Suppression de la base de données de production..."
    rm "$TEST_DIR/fitgang.db"
fi

# Créer un fichier .env de test
echo "   Création du fichier .env de test..."
cat > "$TEST_DIR/.env" << 'EOF'
# Configuration FitGang - ENVIRONNEMENT DE TEST
SECRET_KEY=test_secret_key_change_this_in_production
DATABASE_URL=sqlite:///fitgang_test.db
BASE_URL=https://test.fitgang.fr
FLASK_ENV=development
FLASK_DEBUG=True

# Stripe TEST mode (remplace par tes vraies clés de test Stripe)
STRIPE_PUBLIC_KEY=pk_test_CHANGE_ME
STRIPE_SECRET_KEY=sk_test_CHANGE_ME
STRIPE_WEBHOOK_SECRET=whsec_test_CHANGE_ME

# Email (optionnel)
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=test@example.com
MAIL_PASSWORD=password
EOF

echo "✅ Fichier .env créé"
echo ""

echo "3️⃣  Création du fichier passenger_wsgi.py pour test..."
echo ""

cat > "$TEST_DIR/passenger_wsgi.py" << 'EOF'
import sys
import os

# Chemin vers l'interpréteur Python du virtualenv
INTERP = "/home/wrbh3411/virtualenv/test.fitgang.fr/3.6/bin/python3"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Ajouter le répertoire de l'application au path
sys.path.insert(0, os.path.dirname(__file__))

# Importer et créer l'application Flask
from app import create_app
application = create_app('default')
EOF

echo "✅ passenger_wsgi.py créé"
echo ""

echo "4️⃣  Création de la structure tmp/..."
mkdir -p "$TEST_DIR/tmp"
echo "✅ Dossier tmp créé"
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "  Configuration presque terminée!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📋 PROCHAINES ÉTAPES:"
echo ""
echo "1. Va dans cPanel o2switch et crée le sous-domaine 'test.fitgang.fr'"
echo "   - Sous-domaines → Créer"
echo "   - Sous-domaine: test"
echo "   - Racine: $TEST_DIR"
echo ""
echo "2. Modifie le fichier .env avec tes vraies clés Stripe de TEST:"
echo "   nano $TEST_DIR/.env"
echo ""
echo "3. Initialise la base de données:"
echo "   cd $TEST_DIR"
echo "   python init_db.py"
echo ""
echo "4. Redémarre l'application:"
echo "   cd $TEST_DIR"
echo "   touch tmp/restart.txt"
echo ""
echo "5. Teste dans ton navigateur:"
echo "   https://test.fitgang.fr"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "✅ Script terminé avec succès!"
echo ""
