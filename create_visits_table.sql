-- Création de la table visits pour le système analytics
-- À exécuter si flask db migrate ne fonctionne pas

CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address VARCHAR(50),
    user_agent VARCHAR(500),
    page VARCHAR(500),
    referer VARCHAR(500),
    user_id INTEGER,
    session_id VARCHAR(100),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    country VARCHAR(100),
    city VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS ix_visits_session_id ON visits (session_id);
CREATE INDEX IF NOT EXISTS ix_visits_timestamp ON visits (timestamp);
CREATE INDEX IF NOT EXISTS ix_visits_user_id ON visits (user_id);

-- Vérification
SELECT 'Table visits créée avec succès!' AS result;
