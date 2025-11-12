-- Script SQL pour créer la table blog_posts
-- À exécuter sur test.fitgang.fr

-- Création de la table blog_posts
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

-- Création des index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_blog_slug ON blog_posts(slug);
CREATE INDEX IF NOT EXISTS idx_blog_publie ON blog_posts(publie);
CREATE INDEX IF NOT EXISTS idx_blog_date ON blog_posts(date_publication);

-- Vérification
SELECT 'Table blog_posts créée avec succès!' AS message;
SELECT COUNT(*) as nb_tables FROM sqlite_master WHERE type='table' AND name='blog_posts';
