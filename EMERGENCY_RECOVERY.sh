#!/bin/bash
# ⚠️  EMERGENCY RECOVERY SCRIPT ⚠️
# Restaure fitgang.fr à un état stable (SANS le blog pour l'instant)
# À exécuter sur le serveur: bash EMERGENCY_RECOVERY.sh

set -e  # Stop on any error

echo "🚨 === RÉCUPÉRATION D'URGENCE DE FITGANG.FR ==="
echo ""

cd /home/wrbh3411/fitgang.fr

# Backup de sécurité si des fichiers existent encore
echo "1. Backup de sécurité..."
mkdir -p emergency_backup_$(date +%Y%m%d_%H%M%S)
cp -r app emergency_backup_$(date +%Y%m%d_%H%M%S)/ 2>/dev/null || echo "  (pas de app/ à sauvegarder)"
cp config.py emergency_backup_$(date +%Y%m%d_%H%M%S)/ 2>/dev/null || echo "  (pas de config.py à sauvegarder)"
cp passenger_wsgi.py emergency_backup_$(date +%Y%m%d_%H%M%S)/ 2>/dev/null || echo "  (pas de passenger_wsgi.py à sauvegarder)"

# Téléchargement de la version stable depuis GitHub
echo ""
echo "2. Téléchargement de la version stable depuis GitHub..."
echo "   (commit 503eff5 - version stable AVANT le blog)"
curl -L https://github.com/max0067/fitgang/archive/503eff5.tar.gz -o recovery_stable.tar.gz

echo ""
echo "3. Extraction des fichiers..."
tar -xzf recovery_stable.tar.gz

# Restauration du dossier app/
echo ""
echo "4. Restauration du dossier app/..."
rm -rf app 2>/dev/null || true
cp -r fitgang-503eff5/app .
echo "   ✅ app/ restauré"

# Restauration des fichiers critiques
echo ""
echo "5. Restauration des fichiers critiques..."
cp fitgang-503eff5/config.py .
cp fitgang-503eff5/passenger_wsgi.py .
echo "   ✅ config.py et passenger_wsgi.py restaurés"

# Vérifier que .env existe
if [ ! -f .env ]; then
    echo ""
    echo "6. Création de .env manquant..."
    cat > .env << 'EOF'
SECRET_KEY=fitgang-production-secret-key-2024
DATABASE_URL=sqlite:///fitgang.db
FLASK_ENV=production
EOF
    echo "   ✅ .env créé"
else
    echo ""
    echo "6. .env existe déjà ✅"
fi

# Nettoyage
echo ""
echo "7. Nettoyage des fichiers temporaires..."
rm -rf fitgang-503eff5 recovery_stable.tar.gz
echo "   ✅ Nettoyé"

# RESTART AGRESSIF de Passenger
echo ""
echo "8. Redémarrage COMPLET de Passenger..."
pkill -9 python 2>/dev/null || echo "   (aucun processus Python à tuer)"
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
rm -rf tmp 2>/dev/null || true
mkdir -p tmp
touch passenger_wsgi.py
echo "$(date)" > tmp/restart.txt
echo "   ✅ Passenger redémarré"

# Attente du redémarrage
echo ""
echo "9. Attente du redémarrage (30 secondes)..."
sleep 30

# Tests
echo ""
echo "=== TESTS DE VÉRIFICATION ==="
echo ""
echo "Test 1: Page d'accueil"
HOMEPAGE=$(curl -k -I -s https://fitgang.fr/ 2>/dev/null | head -n 1)
echo "   $HOMEPAGE"

echo ""
echo "Test 2: Dashboard"
DASHBOARD=$(curl -k -I -s https://fitgang.fr/dashboard 2>/dev/null | head -n 1)
echo "   $DASHBOARD"

echo ""
echo "Test 3: Structure des fichiers"
echo -n "   app/ existe: "
[ -d app ] && echo "✅ OUI" || echo "❌ NON"

echo -n "   config.py existe: "
[ -f config.py ] && echo "✅ OUI" || echo "❌ NON"

echo -n "   .env existe: "
[ -f .env ] && echo "✅ OUI" || echo "❌ NON"

echo ""
echo "=== RÉSULTAT ==="
if [ -d app ] && [ -f config.py ]; then
    echo "✅ ✅ ✅ RÉCUPÉRATION RÉUSSIE ! ✅ ✅ ✅"
    echo ""
    echo "Le site devrait être de retour en ligne."
    echo "Vérifie https://fitgang.fr et https://fitgang.fr/dashboard"
    echo ""
    echo "⚠️  NOTE: Le blog n'est PAS encore déployé (version stable sans blog)"
    echo "   On s'occupera du blog séparément une fois le site stable."
else
    echo "❌ ÉCHEC - Vérifie les erreurs ci-dessus"
fi

echo ""
echo "=== TERMINÉ ==="
