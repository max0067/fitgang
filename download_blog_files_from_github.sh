#!/bin/bash
# Script pour télécharger les fichiers blog depuis GitHub sur test.fitgang.fr
# À exécuter sur le serveur dans /home/wrbh3411/test.fitgang.fr

echo "🏋️ Téléchargement des fichiers blog depuis GitHub..."

# URL de base pour les fichiers bruts sur GitHub
GITHUB_RAW="https://raw.githubusercontent.com/max0067/fitgang/claude/fix-email-campaigns-011CV29exAWnnTfzcJ4vZoRk"

cd /home/wrbh3411/test.fitgang.fr

# Backup des fichiers existants
echo "1. Backup des fichiers existants..."
mkdir -p backups
cp app/models.py backups/models.py.backup 2>/dev/null
cp config.py backups/config.py.backup 2>/dev/null
cp app/routes.py backups/routes.py.backup 2>/dev/null
cp app/templates/base.html backups/base.html.backup 2>/dev/null

# Téléchargement des fichiers principaux
echo "2. Téléchargement de models.py (avec BlogPost)..."
curl -f -s -o app/models.py "$GITHUB_RAW/app/models.py"

echo "3. Téléchargement de config.py (avec TEMPLATES_AUTO_RELOAD)..."
curl -f -s -o config.py "$GITHUB_RAW/config.py"

echo "4. Téléchargement de routes.py (avec routes blog)..."
curl -f -s -o app/routes.py "$GITHUB_RAW/app/routes.py"

echo "5. Téléchargement de forms.py (avec BlogPostForm)..."
curl -f -s -o app/forms.py "$GITHUB_RAW/app/forms.py"

echo "6. Téléchargement de base.html (avec nouveaux menus dropdown)..."
curl -f -s -o app/templates/base.html "$GITHUB_RAW/app/templates/base.html"

# Téléchargement des templates blog
echo "7. Téléchargement des templates blog..."
curl -f -s -o app/templates/blog.html "$GITHUB_RAW/app/templates/blog.html"
curl -f -s -o app/templates/blog_article.html "$GITHUB_RAW/app/templates/blog_article.html"
curl -f -s -o app/templates/admin_blog.html "$GITHUB_RAW/app/templates/admin_blog.html"
curl -f -s -o app/templates/admin_blog_form.html "$GITHUB_RAW/app/templates/admin_blog_form.html"

echo "✅ Fichiers téléchargés avec succès"

# Vérifications
echo ""
echo "=== VÉRIFICATIONS ==="
echo -n "BlogPost dans models.py: "
grep -c "class BlogPost" app/models.py

echo -n "TEMPLATES_AUTO_RELOAD dans config.py: "
grep -c "TEMPLATES_AUTO_RELOAD" config.py

echo -n "Routes blog dans routes.py: "
grep -c "def blog" app/routes.py

echo -n "Dropdowns dans base.html: "
grep -c "dropdown" app/templates/base.html

echo -n "Template blog.html existe: "
[ -f app/templates/blog.html ] && echo "OUI" || echo "NON"

# Création de la table blog_posts
echo ""
echo "8. Création de la table blog_posts..."
sqlite3 fitgang.db << 'EOSQL'
CREATE TABLE IF NOT EXISTS blog_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(300) NOT NULL,
    slug VARCHAR(350) NOT NULL UNIQUE,
    meta_description VARCHAR(160) NOT NULL,
    contenu TEXT NOT NULL,
    image VARCHAR(300),
    auteur VARCHAR(100) DEFAULT 'FitGang Team',
    publie BOOLEAN DEFAULT 0,
    featured BOOLEAN DEFAULT 0,
    date_publication DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP,
    vues INTEGER DEFAULT 0,
    tags VARCHAR(500),
    categorie VARCHAR(100)
);
CREATE INDEX IF NOT EXISTS idx_blog_slug ON blog_posts(slug);
CREATE INDEX IF NOT EXISTS idx_blog_publie ON blog_posts(publie);
EOSQL

echo -n "Table blog_posts créée: "
sqlite3 fitgang.db "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='blog_posts';"

# Nettoyage des caches
echo ""
echo "9. Nettoyage des caches..."
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
rm -rf tmp/*
mkdir -p tmp
touch passenger_wsgi.py
echo "$(date)" > tmp/restart.txt

echo "✅ Caches nettoyés et application redémarrée"

# Attendre le redémarrage
echo ""
echo "10. Attente du redémarrage (15 secondes)..."
sleep 15

# Tests finaux
echo ""
echo "=== TESTS FINAUX ==="
echo -n "Page d'accueil: "
curl -k -I -s https://test.fitgang.fr/ | head -n 1

echo -n "Page blog: "
curl -k -I -s https://test.fitgang.fr/blog | head -n 1

echo ""
echo -n "Nouveau header visible (dropdowns dans HTML): "
DROPDOWN_COUNT=$(curl -k -s https://test.fitgang.fr/ 2>/dev/null | grep -c "dropdown")
echo "$DROPDOWN_COUNT occurrences"

if [ "$DROPDOWN_COUNT" -gt 30 ]; then
    echo "✅ ✅ ✅ SUCCÈS ! Le nouveau header est visible ! ✅ ✅ ✅"
else
    echo "⚠️  Le cache persiste. Essaie d'ouvrir https://test.fitgang.fr en navigation privée"
fi

echo ""
echo "=== TERMINÉ ==="
echo "Ouvre https://test.fitgang.fr dans ton navigateur pour voir le résultat !"
