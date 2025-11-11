#!/bin/bash
# Script d'installation des dépendances dans le virtualenv cPanel

echo "🔧 Installation des dépendances dans le virtualenv cPanel..."

# Activer le virtualenv cPanel
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate

# Vérifier que nous sommes dans le bon virtualenv
echo "📍 Python utilisé: $(which python3)"
echo "📍 Pip utilisé: $(which pip)"

# Aller dans le répertoire du projet
cd /home/wrbh3411/fitgang.fr

# Installer python-dotenv en premier (dépendance critique manquante)
echo "📦 Installation de python-dotenv..."
pip install python-dotenv==0.19.2

# Installer toutes les dépendances
echo "📦 Installation de toutes les dépendances..."
pip install -r requirements.txt

# Vérifier que dotenv est bien installé
echo ""
echo "✅ Vérification de l'installation..."
python3 -c "import dotenv; print('✅ python-dotenv est installé')" || echo "❌ python-dotenv n'est pas installé"
python3 -c "import flask; print('✅ Flask est installé')" || echo "❌ Flask n'est pas installé"
python3 -c "import flask_login; print('✅ Flask-Login est installé')" || echo "❌ Flask-Login n'est pas installé"

# Créer le fichier .env s'il n'existe pas
if [ ! -f .env ]; then
    echo ""
    echo "📝 Création du fichier .env..."
    cp production.env.example .env
    # Générer une vraie SECRET_KEY
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    sed -i "s/GENERER_UNE_NOUVELLE_CLE_SECRETE_ICI/$SECRET_KEY/" .env
    sed -i "s|https://fitgang.fr|https://fitgang.fr|" .env
    echo "✅ Fichier .env créé"
else
    echo "✅ Le fichier .env existe déjà"
fi

# Tester que l'application Flask peut se charger
echo ""
echo "🧪 Test de l'application Flask..."
python3 -c "
import sys
sys.path.insert(0, '/home/wrbh3411/fitgang.fr')
from dotenv import load_dotenv
load_dotenv('.env')
from app import create_app
app = create_app('production')
print('✅ Application Flask chargée avec succès!')
" || echo "❌ Erreur lors du chargement de l'application"

# Redémarrer Passenger
echo ""
echo "🔄 Redémarrage de Passenger..."
mkdir -p tmp
touch tmp/restart.txt

echo ""
echo "✅ INSTALLATION TERMINÉE!"
echo "🌐 Va sur https://fitgang.fr pour tester"
