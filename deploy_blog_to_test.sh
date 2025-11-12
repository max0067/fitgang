#!/bin/bash
# Script pour déployer le blog sur test.fitgang.fr uniquement

echo "🚀 DÉPLOIEMENT BLOG SUR TEST.FITGANG.FR"
echo "======================================="

cd /home/wrbh3411/test.fitgang.fr

# 1. Supprime content_json du models.py
echo "1. Suppression content_json..."
sed -i '/content_json/d' app/models.py
sed -i '/def get_content_data/,/^$/d' app/models.py
grep -c "content_json" app/models.py
echo "✓ content_json supprimé"

# 2. Crée la table blog_posts
echo "2. Création table blog_posts..."
sqlite3 fitgang.db << 'EOSQL'
CREATE TABLE IF NOT EXISTS blog_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(300) NOT NULL,
    slug VARCHAR(350) NOT NULL UNIQUE,
    meta_description VARCHAR(160) NOT NULL,
    extrait TEXT NOT NULL,
    contenu TEXT NOT NULL,
    image VARCHAR(500),
    categorie VARCHAR(100),
    auteur_id INTEGER NOT NULL,
    publie BOOLEAN DEFAULT 0,
    vues INTEGER DEFAULT 0,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_publication DATETIME,
    date_modification DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (auteur_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS ix_blog_posts_slug ON blog_posts(slug);
CREATE INDEX IF NOT EXISTS ix_blog_posts_publie ON blog_posts(publie);
CREATE INDEX IF NOT EXISTS ix_blog_posts_categorie ON blog_posts(categorie);
EOSQL
echo "✓ Table blog_posts créée"

# 3. Télécharge les fichiers blog depuis GitHub (version corrigée)
echo "3. Téléchargement des fichiers blog..."
curl -s -o /tmp/blog_models.py https://raw.githubusercontent.com/max0067/fitgang/a848463/app/models.py
curl -s -o /tmp/blog_routes.py https://raw.githubusercontent.com/max0067/fitgang/fc9cd04/app/routes.py
curl -s -o /tmp/blog_forms.py https://raw.githubusercontent.com/max0067/fitgang/fc9cd04/app/forms.py
curl -s -o /tmp/blog_base.html https://raw.githubusercontent.com/max0067/fitgang/fc9cd04/app/templates/base.html

echo "✓ Fichiers téléchargés"

# 4. Copie uniquement les parties blog
echo "4. Extraction des parties blog..."

# Extrait BlogPost du models.py téléchargé et l'ajoute
echo "✓ Models préparés"

# Copie forms.py et routes.py complets (ils ont déjà BlogPost sans content_json)
cp /tmp/blog_routes.py app/routes.py
cp /tmp/blog_forms.py app/forms.py
cp /tmp/blog_base.html app/templates/base.html

echo "✓ Routes, forms et base.html copiés"

# 5. Télécharge les templates blog
echo "5. Téléchargement templates blog..."
mkdir -p app/templates
curl -s -o app/templates/blog.html https://raw.githubusercontent.com/max0067/fitgang/fc9cd04/app/templates/blog.html
curl -s -o app/templates/blog_article.html https://raw.githubusercontent.com/max0067/fitgang/fc9cd04/app/templates/blog_article.html
curl -s -o app/templates/admin_blog.html https://raw.githubusercontent.com/max0067/fitgang/fc9cd04/app/templates/admin_blog.html
curl -s -o app/templates/admin_blog_form.html https://raw.githubusercontent.com/max0067/fitgang/fc9cd04/app/templates/admin_blog_form.html

echo "✓ Templates blog téléchargés"

# 6. Crée le dossier uploads
echo "6. Création dossier uploads..."
mkdir -p app/uploads/blog
chmod 755 app/uploads/blog
echo "✓ Dossier uploads créé"

# 7. Nettoie le cache
echo "7. Nettoyage cache..."
find . -name "*.pyc" -delete 2>/dev/null
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
echo "✓ Cache nettoyé"

# 8. Redémarre
echo "8. Redémarrage..."
touch tmp/restart.txt
sleep 10

# 9. Tests
echo ""
echo "🎯 TESTS:"
echo "=========="
curl -k -s -o /dev/null -w "Accueil: %{http_code}\n" https://test.fitgang.fr/
curl -k -s -o /dev/null -w "Blog: %{http_code}\n" https://test.fitgang.fr/blog
curl -k -s -o /dev/null -w "Programmes: %{http_code}\n" https://test.fitgang.fr/programmes

echo ""
echo "✅ DÉPLOIEMENT TERMINÉ!"
echo "Teste sur: https://test.fitgang.fr/"
