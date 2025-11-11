"""
Fichier WSGI pour o2switch/Passenger
Version avec gestion d'erreurs détaillée
"""
import sys
import os
import traceback

# Ajouter le répertoire du projet au path
sys.path.insert(0, os.getcwd())

def application(environ, start_response):
    """
    Point d'entrée WSGI pour Passenger
    Affiche les erreurs détaillées pour faciliter le débogage
    """
    try:
        # Charger les variables d'environnement
        from dotenv import load_dotenv
        load_dotenv('.env')

        # Créer l'application Flask
        from app import create_app
        flask_app = create_app('production')

        # Appeler l'application Flask
        return flask_app(environ, start_response)

    except Exception as e:
        # En cas d'erreur, afficher un message détaillé
        error_text = traceback.format_exc()

        # Page HTML avec l'erreur
        error_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Erreur de démarrage - FitGang</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            padding: 20px;
            background: #0a0a0a;
            color: #ff4444;
        }}
        h1 {{
            color: #ff4444;
            border-bottom: 2px solid #ff4444;
            padding-bottom: 10px;
        }}
        pre {{
            background: #1a1a1a;
            padding: 20px;
            border: 2px solid #ff4444;
            border-radius: 5px;
            overflow: auto;
            color: #ffffff;
        }}
        .info {{
            background: #1a3a1a;
            border: 1px solid #44ff44;
            color: #44ff44;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <h1>🏋️ FitGang - Erreur de Démarrage</h1>

    <div class="info">
        <strong>Informations de debug:</strong><br>
        Python: {sys.version}<br>
        Chemin: {os.getcwd()}<br>
        sys.path: {sys.path[:3]}
    </div>

    <h2>Erreur détaillée:</h2>
    <pre>{error_text}</pre>

    <p>
        <strong>Solutions possibles:</strong><br>
        1. Vérifier que toutes les dépendances sont installées: source venv/bin/activate && pip install -r requirements.txt<br>
        2. Vérifier que le fichier .env existe et contient DATABASE_URL<br>
        3. Vérifier les logs: tail -f ~/logs/error.log
    </p>
</body>
</html>"""

        # Retourner la page d'erreur
        status = '200 OK'
        response_headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, response_headers)
        return [error_html.encode('utf-8')]
