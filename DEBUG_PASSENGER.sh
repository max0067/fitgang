#!/bin/bash
# DEBUG PASSENGER - Affiche l'erreur exacte

cd /home/wrbh3411/fitgang.fr

echo "🔍 Mode DEBUG Passenger..."

# Créer un passenger_wsgi.py qui affiche les erreurs
cat > passenger_wsgi.py << 'WSGIEOF'
import sys
import os
import site
import traceback

def application(environ, start_response):
    try:
        # Ajouter les packages --user
        user_site = site.getusersitepackages()
        if user_site not in sys.path:
            sys.path.insert(0, user_site)

        sys.path.insert(0, os.path.dirname(__file__))

        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

        from app import create_app
        flask_app = create_app('production')

        return flask_app(environ, start_response)

    except Exception as e:
        error_html = f"""<!DOCTYPE html>
<html>
<head><title>DEBUG Passenger</title></head>
<body style="font-family: monospace; padding: 20px;">
<h1>🔍 DEBUG PASSENGER</h1>
<h2>Erreur:</h2>
<pre style="background: #f0f0f0; padding: 10px;">{traceback.format_exc()}</pre>
<h2>Python Info:</h2>
<pre>
Python: {sys.version}
Executable: {sys.executable}
User site: {site.getusersitepackages()}
</pre>
<h2>sys.path:</h2>
<pre>{'<br>'.join(sys.path)}</pre>
</body>
</html>"""

        status = '200 OK'
        response_headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, response_headers)
        return [error_html.encode('utf-8')]
WSGIEOF

# Redémarrer
echo "🔄 Redémarrage..."
pkill -9 python 2>/dev/null
touch passenger_wsgi.py
mkdir -p tmp
echo "$(date)" > tmp/restart.txt
sleep 10

echo ""
echo "✅ Mode debug activé"
echo ""
echo "Ouvre maintenant https://fitgang.fr dans ton navigateur"
echo "Tu verras l'erreur EXACTE affichée sur la page"
echo ""
