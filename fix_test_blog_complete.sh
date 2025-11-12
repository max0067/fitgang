#!/bin/bash
# Script complet pour réparer le blog sur test.fitgang.fr
# Ajoute le modèle BlogPost et force le rechargement des templates

echo "🏋️ Fix complet du blog sur test.fitgang.fr..."

cd /home/wrbh3411/test.fitgang.fr

# 1. Backup models.py
echo "1. Backup de models.py..."
cp app/models.py app/models.py.backup

# 2. Ajouter le modèle BlogPost à la fin de models.py
echo "2. Ajout du modèle BlogPost..."
cat >> app/models.py << 'EOFMODEL'


class BlogPost(db.Model):
    """
    Modèle article de blog
    Gestion des articles de blog avec SEO optimisé
    """
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(300), nullable=False)
    slug = db.Column(db.String(350), unique=True, nullable=False, index=True)
    meta_description = db.Column(db.String(160), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(300))  # URL ou chemin de l'image principale
    auteur = db.Column(db.String(100), default="FitGang Team")
    publie = db.Column(db.Boolean, default=False)
    featured = db.Column(db.Boolean, default=False)  # Article mis en avant
    date_publication = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    vues = db.Column(db.Integer, default=0)

    # Tags et catégories
    tags = db.Column(db.String(500))  # Tags séparés par des virgules
    categorie = db.Column(db.String(100))  # Nutrition, Entraînement, Suppléments, etc.

    def __repr__(self):
        return f'<BlogPost {self.titre}>'

    def increment_views(self):
        """Incrémente le nombre de vues"""
        self.vues += 1
        db.session.commit()

    def get_tags_list(self):
        """Retourne les tags sous forme de liste"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
EOFMODEL

echo "✅ Modèle BlogPost ajouté à models.py"

# 3. Créer/vérifier la table blog_posts
echo "3. Création de la table blog_posts dans la base de données..."
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

echo "✅ Table blog_posts créée/vérifiée"

# 4. CACHE CLEARING AGRESSIF
echo "4. Nettoyage agressif de tous les caches..."

# Supprimer tous les .pyc et __pycache__
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Supprimer le dossier tmp complètement et le recréer
rm -rf tmp/
mkdir -p tmp/restart_dir
touch tmp/restart.txt

# Modifier le fichier config.py pour forcer le reload
if ! grep -q "TEMPLATES_AUTO_RELOAD" config.py; then
    echo "" >> config.py
    echo "# Force template reload" >> config.py
    echo "TEMPLATES_AUTO_RELOAD = True" >> config.py
fi

# Modifier le timestamp de base.html pour forcer Flask à le recharger
touch app/templates/base.html

# Tuer tous les processus Python liés à test.fitgang
pkill -f "test.fitgang" 2>/dev/null
sleep 3

# Créer un fichier restart avec timestamp pour forcer Passenger à redémarrer
echo "$(date)" > tmp/restart.txt

echo "✅ Tous les caches nettoyés"

# 5. Attendre le redémarrage
echo "5. Attente du redémarrage de l'application..."
sleep 10

# 6. Tests de vérification
echo ""
echo "=== VÉRIFICATIONS ==="
echo "6. Test des fichiers et base de données..."

echo -n "BlogPost dans models.py: "
grep -c "class BlogPost" app/models.py

echo -n "Table blog_posts existe: "
sqlite3 fitgang.db "SELECT name FROM sqlite_master WHERE type='table' AND name='blog_posts';" | wc -l

echo -n "Routes blog dans routes.py: "
grep -c "def blog" app/routes.py

echo -n "Dropdowns dans base.html: "
grep -c "dropdown" app/templates/base.html

echo ""
echo "7. Test HTTP des pages..."
sleep 5

echo -n "Page d'accueil: "
curl -k -I -s https://test.fitgang.fr/ | head -n 1

echo -n "Page blog: "
curl -k -I -s https://test.fitgang.fr/blog | head -n 1

echo ""
echo "8. Test du nouveau header (dropdowns dans HTML)..."
DROPDOWN_COUNT=$(curl -k -s https://test.fitgang.fr/ 2>/dev/null | grep -c "dropdown")
echo "Nombre de 'dropdown' dans le HTML servi: $DROPDOWN_COUNT"

if [ "$DROPDOWN_COUNT" -gt 0 ]; then
    echo "✅ ✅ ✅ NOUVEAU HEADER DÉTECTÉ! ✅ ✅ ✅"
else
    echo "⚠️  Le cache persiste encore, tentative de force restart..."
    # Dernier recours: modifier passenger_wsgi.py pour forcer le rechargement
    touch passenger_wsgi.py
    rm -rf tmp/*
    mkdir -p tmp
    echo "$(date)" > tmp/restart.txt
    sleep 15
    DROPDOWN_COUNT=$(curl -k -s https://test.fitgang.fr/ 2>/dev/null | grep -c "dropdown")
    echo "Nouveau test - Dropdowns dans HTML: $DROPDOWN_COUNT"
fi

echo ""
echo "=== FIN DU SCRIPT ==="
echo "Si les tests montrent des dropdowns, le nouveau header fonctionne!"
echo "Si blog retourne 200 OK, le blog est opérationnel!"
