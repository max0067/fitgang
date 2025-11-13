#!/bin/bash
# ACTIVER LES LOGS PASSENGER pour voir l'erreur exacte

cd /home/wrbh3411/fitgang.fr

echo "🔍 Activation des logs Passenger..."

# .htaccess avec logs activés
cat > .htaccess << 'HTEOF'
PassengerEnabled on
PassengerPython /home/wrbh3411/fitgang.fr/venv/bin/python3
PassengerAppRoot /home/wrbh3411/fitgang.fr
PassengerStartupFile passenger_wsgi.py
PassengerAppEnv development
PassengerFriendlyErrorPages on
PassengerAppLogFile /home/wrbh3411/fitgang.fr/passenger_error.log
SetEnv FLASK_ENV production
HTEOF

echo "✅ Logs activés dans .htaccess"
echo ""

# Créer le fichier de log
touch passenger_error.log
chmod 644 passenger_error.log

# Redémarrer
echo "🔄 Redémarrage Passenger..."
pkill -9 python 2>/dev/null
touch passenger_wsgi.py
mkdir -p tmp && echo "$(date)" > tmp/restart.txt
sleep 5

# Forcer une requête pour générer des logs
echo ""
echo "📡 Envoi d'une requête pour générer des logs..."
curl -s https://fitgang.fr/ > /dev/null 2>&1
sleep 3

# Afficher les logs
echo ""
echo "=== LOGS PASSENGER ==="
if [ -f passenger_error.log ]; then
    tail -100 passenger_error.log
else
    echo "⚠️  Fichier de log non créé"
fi

echo ""
echo "=== INSTRUCTIONS ==="
echo "1. Lis les logs ci-dessus"
echo "2. Envoie-moi l'erreur exacte"
echo "3. Pour voir les logs en temps réel: tail -f passenger_error.log"
