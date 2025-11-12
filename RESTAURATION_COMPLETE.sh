#!/bin/bash
# RESTAURATION COMPLETE DE FITGANG.FR
# Script tout-en-un - exécuter et c'est fini

set -e

echo "🚨 RESTAURATION COMPLETE DE FITGANG.FR"
echo ""

cd /home/wrbh3411/fitgang.fr

# Nettoyage complet
echo "1. Nettoyage..."
rm -rf app 2>/dev/null || true
rm -rf fitgang-* 2>/dev/null || true
rm -f recovery*.tar.gz 2>/dev/null || true
pkill -9 python 2>/dev/null || true

# Téléchargement version stable
echo ""
echo "2. Téléchargement version stable (commit 6f5adc1)..."
curl -L https://github.com/max0067/fitgang/archive/6f5adc1acffb6b682f8948331e9df6f3ffc3cbf2.tar.gz -o stable.tar.gz

# Extraction
echo ""
echo "3. Extraction..."
tar -xzf stable.tar.gz

# Détection auto du nom du dossier
FOLDER=$(ls -d fitgang-* 2>/dev/null | head -n 1)

if [ -z "$FOLDER" ]; then
    echo "❌ ERREUR: Dossier non trouvé après extraction"
    exit 1
fi

echo "   Dossier trouvé: $FOLDER"

# Copie des fichiers
echo ""
echo "4. Restauration des fichiers..."
cp -r "$FOLDER/app" .
cp "$FOLDER/config.py" .
cp "$FOLDER/passenger_wsgi.py" .
cp "$FOLDER/.htaccess" . 2>/dev/null || true
echo "   ✅ Fichiers copiés"

# Création du .env
echo ""
echo "5. Configuration .env..."
cat > .env << 'ENVEOF'
SECRET_KEY=fitgang-production-secret-key-2024
DATABASE_URL=sqlite:///fitgang.db
FLASK_ENV=production
MAIL_SERVER=mail.fitgang.fr
MAIL_PORT=465
MAIL_USE_SSL=true
MAIL_USERNAME=admin@fitgang.fr
MAIL_DEFAULT_SENDER=admin@fitgang.fr
ADMIN_EMAIL=admin@fitgang.fr
ENVEOF
echo "   ✅ .env créé"

# Vérification de la base de données
echo ""
echo "6. Vérification base de données..."
if [ ! -f fitgang.db ]; then
    echo "   ⚠️  Base de données manquante - création d'une nouvelle"
    sqlite3 fitgang.db "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY);"
fi
echo "   ✅ Base de données OK"

# Nettoyage
echo ""
echo "7. Nettoyage..."
rm -rf "$FOLDER" stable.tar.gz
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
rm -rf tmp 2>/dev/null || true
mkdir -p tmp
echo "   ✅ Nettoyé"

# Redémarrage BRUTAL de Passenger
echo ""
echo "8. Redémarrage Passenger..."
touch passenger_wsgi.py
echo "$(date)" > tmp/restart.txt
sleep 5
pkill -9 python 2>/dev/null || true
sleep 5
touch passenger_wsgi.py
echo "   ✅ Passenger redémarré"

# Attente et test
echo ""
echo "9. Attente 30 secondes..."
sleep 30

echo ""
echo "10. Test du site..."
HTTP_CODE=$(curl -k -s -o /dev/null -w "%{http_code}" https://fitgang.fr/ --max-time 15)

echo ""
echo "=== RÉSULTAT ==="
echo "Code HTTP: $HTTP_CODE"

if [ "$HTTP_CODE" = "200" ]; then
    echo ""
    echo "✅ ✅ ✅ SUCCÈS TOTAL ! ✅ ✅ ✅"
    echo ""
    echo "Le site est EN LIGNE: https://fitgang.fr"
    echo ""
else
    echo ""
    echo "⚠️  Code HTTP: $HTTP_CODE"
    echo "Vérifie manuellement: https://fitgang.fr"
    echo ""
    echo "Si erreur 500, vérifie:"
    echo "  - cat /home/wrbh3411/fitgang.fr/passenger_wsgi.py"
    echo "  - ls -la /home/wrbh3411/fitgang.fr/app/"
fi

echo ""
echo "=== FICHIERS RESTAURÉS ==="
ls -lh app/ config.py passenger_wsgi.py .env fitgang.db 2>/dev/null || true

echo ""
echo "=== TERMINÉ ==="
