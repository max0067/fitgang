# 🏋️ Déploiement du Blog sur test.fitgang.fr

## ✅ Ce qui a été fait

Les modifications suivantes ont été poussées sur GitHub :

1. **BlogPost model** ajouté dans `app/models.py` avec :
   - Titres, slugs, méta descriptions SEO
   - Support des images
   - Tags et catégories
   - Compteur de vues
   - Gestion published/draft

2. **Template auto-reload** activé dans `config.py`
   - Résout les problèmes de cache des templates
   - Les modifications HTML seront visibles immédiatement

3. **Script de déploiement** : `fix_test_blog_complete.sh`
   - Ajoute le modèle BlogPost
   - Crée la table blog_posts
   - Nettoie tous les caches agressivement
   - Redémarre Passenger

## 📋 Instructions de Déploiement

### Option 1 : Via SSH (Recommandé)

Connecte-toi à ton serveur o2switch et exécute :

```bash
# 1. Aller dans le dossier test
cd /home/wrbh3411/test.fitgang.fr

# 2. Récupérer les dernières modifications depuis GitHub
git pull origin claude/fix-email-campaigns-011CV29exAWnnTfzcJ4vZoRk

# 3. Rendre le script exécutable
chmod +x fix_test_blog_complete.sh

# 4. Exécuter le script de déploiement
./fix_test_blog_complete.sh
```

Le script va :
- ✅ Ajouter le modèle BlogPost à models.py
- ✅ Créer la table blog_posts dans la base de données
- ✅ Nettoyer tous les caches Python (.pyc, __pycache__)
- ✅ Forcer le rechargement des templates
- ✅ Redémarrer Passenger
- ✅ Tester que tout fonctionne

### Option 2 : Via FTP/cPanel

Si tu n'as pas accès SSH :

1. **Télécharger les fichiers depuis GitHub** :
   - `app/models.py` (avec BlogPost)
   - `config.py` (avec TEMPLATES_AUTO_RELOAD)
   - `fix_test_blog_complete.sh`

2. **Uploader via FTP** dans `/home/wrbh3411/test.fitgang.fr/`

3. **Via l'interface web de o2switch** :
   - Aller dans "Gestionnaire de fichiers"
   - Naviguer vers `/home/wrbh3411/test.fitgang.fr`
   - Clic droit sur `fix_test_blog_complete.sh` → "Execute"

## 🧪 Vérifications Après Déploiement

Une fois le script exécuté, vérifie que :

### 1. Le Blog fonctionne
```bash
curl -I https://test.fitgang.fr/blog
# Devrait retourner : HTTP/2 200
```

### 2. Le Nouveau Header s'affiche
```bash
curl -s https://test.fitgang.fr/ | grep -c "dropdown"
# Devrait retourner un nombre > 0 (environ 37)
```

### 3. Ouvre dans le Navigateur
- Va sur https://test.fitgang.fr
- Tu devrais voir :
  - ✅ Nouveau menu avec dropdowns (Ebooks, Compléments, Mon Profil)
  - ✅ Lien "Blog" dans la navigation
  - ✅ La page /blog devrait s'afficher (vide pour l'instant)

## 🐛 En Cas de Problème

### Le cache persiste encore ?

Si les modifications ne s'affichent toujours pas :

```bash
cd /home/wrbh3411/test.fitgang.fr

# Force restart complet
rm -rf tmp/*
mkdir -p tmp
touch passenger_wsgi.py
touch tmp/restart.txt
sleep 15

# Test
curl -s https://test.fitgang.fr/ | grep -c "dropdown"
```

### Le blog retourne toujours 404 ?

```bash
# Vérifier que le modèle a été ajouté
grep -c "class BlogPost" app/models.py
# Devrait retourner : 1

# Vérifier la table dans la base
sqlite3 fitgang.db "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='blog_posts';"
# Devrait retourner : 1
```

## 📝 Prochaines Étapes

Une fois que test.fitgang.fr fonctionne correctement :

1. **Créer un article de test** via l'admin
2. **Vérifier l'affichage** et le SEO
3. **Si tout est OK**, déployer sur production (fitgang.fr)

## ⚠️ Important

- **NE PAS** toucher à fitgang.fr (production) pour l'instant
- Tous les tests sur test.fitgang.fr uniquement
- La production fonctionne actuellement, ne pas la casser !

## 🆘 Support

Si tu rencontres des problèmes :
1. Vérifie les logs : `tail -f ~/logs/error.log`
2. Exécute les commandes de vérification ci-dessus
3. Partage les résultats pour diagnostic
