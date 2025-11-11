#!/bin/bash

# ========================================
# 🎨 SCRIPT DE MISE À JOUR DU DESIGN
# À exécuter directement sur o2switch
# ========================================

echo ""
echo "======================================"
echo "🎨 MISE À JOUR DESIGN FITGANG"
echo "======================================"
echo ""

# Vérifier qu'on est sur o2switch
if [ ! -d "/home/wrbh3411/fitgang.fr" ]; then
    echo "⚠️  Ce script doit être exécuté sur le serveur o2switch"
    echo "📍 Chemin attendu: /home/wrbh3411/fitgang.fr"
    exit 1
fi

# Aller dans le bon répertoire
cd /home/wrbh3411/fitgang.fr

echo "📂 Répertoire actuel: $(pwd)"
echo ""

# Sauvegarder l'ancien CSS au cas où
echo "💾 Sauvegarde de l'ancien CSS..."
if [ -f "app/static/css/style.css" ]; then
    cp app/static/css/style.css app/static/css/style.css.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup créé"
else
    echo "⚠️  Pas d'ancien CSS trouvé"
fi
echo ""

# Récupérer les changements de GitHub
echo "📥 Récupération des changements depuis GitHub..."
git fetch origin claude/fitgang-fitness-app-011CUzmHxxyY6L1L2RE1vEDx

if [ $? -ne 0 ]; then
    echo "❌ ERREUR lors du fetch"
    echo "Vérifie ta connexion et réessaye"
    exit 1
fi

echo "✅ Fetch réussi"
echo ""

# Pull les changements
echo "🔄 Application des changements..."
git pull origin claude/fitgang-fitness-app-011CUzmHxxyY6L1L2RE1vEDx

if [ $? -ne 0 ]; then
    echo "❌ ERREUR lors du pull"
    echo "Il y a peut-être des conflits"
    echo ""
    echo "🔧 Solution: Reset et re-pull"
    git reset --hard origin/claude/fitgang-fitness-app-011CUzmHxxyY6L1L2RE1vEDx
    if [ $? -ne 0 ]; then
        echo "❌ Reset échoué aussi"
        exit 1
    fi
fi

echo "✅ Changements appliqués"
echo ""

# Vérifier que les fichiers sont là
echo "🔍 Vérification des fichiers..."

if [ -f "app/static/css/style.css" ]; then
    # Vérifier que c'est le nouveau design
    if grep -q "FitGang - Style inspiré BodyTime" app/static/css/style.css; then
        echo "✅ CSS mise à jour (Design BodyTime)"
    else
        echo "⚠️  CSS trouvé mais pas le nouveau design"
    fi
else
    echo "❌ style.css introuvable"
fi

if [ -f "app/templates/base.html" ]; then
    # Vérifier le logo
    if grep -q "height: 65px" app/templates/base.html; then
        echo "✅ base.html mise à jour (Logo 65px)"
    else
        echo "⚠️  base.html trouvé mais logo pas à 65px"
    fi
else
    echo "❌ base.html introuvable"
fi

echo ""

# Vérifier les permissions
echo "🔐 Vérification des permissions..."
chmod 644 app/static/css/style.css
chmod 644 app/templates/base.html
echo "✅ Permissions OK"
echo ""

# Redémarrer Passenger
echo "🔄 Redémarrage de l'application..."
touch tmp/restart.txt

if [ $? -eq 0 ]; then
    echo "✅ Application redémarrée"
else
    echo "❌ Erreur lors du redémarrage"
    exit 1
fi

echo ""
echo "======================================"
echo "✅ MISE À JOUR TERMINÉE !"
echo "======================================"
echo ""
echo "🌐 Va sur: https://fitgang.fr"
echo ""
echo "🔄 N'oublie pas de vider ton cache navigateur:"
echo "   Windows: CTRL + F5"
echo "   Mac: CMD + SHIFT + R"
echo ""
echo "🎨 Tu devrais voir:"
echo "   • Fond noir total (#000000)"
echo "   • Logo à 65px (plus grand)"
echo "   • Boutons rouges (#ED2F2F)"
echo "   • Titres en UPPERCASE"
echo "   • Animation pulse sur les boutons"
echo ""
echo "======================================"
