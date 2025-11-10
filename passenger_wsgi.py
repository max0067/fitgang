"""
Fichier de démarrage pour Passenger (Hostinger)
Ce fichier est utilisé par le serveur Passenger pour lancer l'application Flask
"""
import sys
import os

# Chemin vers l'interpréteur Python du virtualenv
# ⚠️ IMPORTANT: Remplace 'username' par ton vrai username Hostinger
INTERP = os.path.join(os.environ['HOME'], 'public_html', 'venv', 'bin', 'python3')

# Si ce n'est pas le bon interpréteur, relancer avec le bon
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Ajouter le chemin de l'application au sys.path
sys.path.insert(0, os.getcwd())

# Charger les variables d'environnement depuis .env
from dotenv import load_dotenv
project_folder = os.path.expanduser(os.getcwd())
load_dotenv(os.path.join(project_folder, '.env'))

# Importer et créer l'application Flask
from app import create_app

# Créer l'application en mode production
application = create_app('production')

# Pour le debugging en cas de problème (à désactiver en production)
# application.config['DEBUG'] = True
