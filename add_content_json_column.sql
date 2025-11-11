-- Ajout de la colonne content_json au modèle Programme
-- Pour stocker le contenu éditable des pages programmes

ALTER TABLE programmes ADD COLUMN content_json TEXT;

-- Vérification
SELECT id, titre,
       CASE WHEN content_json IS NULL THEN 'Non configuré' ELSE 'Configuré' END as contenu_status
FROM programmes;
