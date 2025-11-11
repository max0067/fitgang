#!/bin/bash

# Script de déploiement du nouveau design FitGang
# Ce script va pousser les changements CSS sur o2switch

echo "======================================"
echo "🎨 DÉPLOIEMENT DU NOUVEAU DESIGN"
echo "======================================"
echo ""

# Vérifier qu'on est dans le bon répertoire
if [ ! -f "app/__init__.py" ]; then
    echo "❌ ERREUR: Exécute ce script depuis le dossier /home/user/fitgang"
    exit 1
fi

echo "📦 Fichiers à déployer:"
echo "  - app/static/css/style.css (Design BodyTime noir/rouge)"
echo "  - app/templates/base.html (Logo 65px + cache buster)"
echo ""

# Vérifier que les fichiers existent
if [ ! -f "app/static/css/style.css" ]; then
    echo "❌ ERREUR: style.css introuvable"
    exit 1
fi

if [ ! -f "app/templates/base.html" ]; then
    echo "❌ ERREUR: base.html introuvable"
    exit 1
fi

echo "✅ Tous les fichiers sont présents"
echo ""

# Commit et push
echo "📤 Envoi des changements vers GitHub..."
git add app/static/css/style.css app/templates/base.html
git commit -m "Design moderne 2024 - Refonte complète du CSS

- Style inspiré BodyTime.fr
- Fond noir total (#000000)
- Accents rouge FitGang (#ED2F2F)
- Logo agrandi à 65px
- Typographie: Rajdhani (titres) + Roboto (texte)
- Tous les titres en UPPERCASE
- Boutons avec animation pulse rouge
- Cards angulaires (pas de border-radius)
- Scrollbar personnalisée rouge
- Cache buster ajouté pour forcer le rechargement CSS"

echo ""
echo "🚀 Push vers o2switch..."
git push -u origin claude/fitgang-fitness-app-011CUzmHxxyY6L1L2RE1vEDx

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✅ DÉPLOIEMENT RÉUSSI !"
    echo "======================================"
    echo ""
    echo "📋 PROCHAINES ÉTAPES SUR O2SWITCH:"
    echo ""
    echo "1️⃣  Connecte-toi en SSH:"
    echo "    ssh wrbh3411@fitgang.fr -p 22"
    echo ""
    echo "2️⃣  Va dans le dossier du site:"
    echo "    cd /home/wrbh3411/fitgang.fr"
    echo ""
    echo "3️⃣  Récupère les changements:"
    echo "    git pull origin claude/fitgang-fitness-app-011CUzmHxxyY6L1L2RE1vEDx"
    echo ""
    echo "4️⃣  Redémarre l'application:"
    echo "    touch tmp/restart.txt"
    echo ""
    echo "5️⃣  Vide le cache de ton navigateur:"
    echo "    Windows: CTRL + F5"
    echo "    Mac: CMD + SHIFT + R"
    echo ""
    echo "🌐 Visite: https://fitgang.fr"
    echo ""
    echo "======================================"
else
    echo ""
    echo "❌ ERREUR lors du push"
    echo "Vérifie ta connexion Internet et réessaye"
    exit 1
fi
