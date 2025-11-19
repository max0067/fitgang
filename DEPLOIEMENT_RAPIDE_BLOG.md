# 🚀 Déploiement Rapide - Blog FitGang

## 📍 Chemin de production
**`/home/wrbh3411/fitgang_app/saas`**

---

## ⚡ Méthode 1: Script automatique (RECOMMANDÉ)

```bash
# Connexion SSH
ssh wrbh3411@votre-serveur.o2switch.net

# Aller dans le dossier
cd /home/wrbh3411/fitgang_app/saas

# Récupérer le script
git pull

# Rendre exécutable et lancer
chmod +x deploy_blog_production.sh
./deploy_blog_production.sh
```

**C'est tout !** Le script fait automatiquement :
- ✅ Git pull
- ✅ Création table `blog_posts`
- ✅ Redémarrage de l'application
- ✅ Vérification

---

## 🔧 Méthode 2: Manuel (ligne par ligne)

```bash
# 1. Connexion
ssh wrbh3411@votre-serveur.o2switch.net

# 2. Navigation
cd /home/wrbh3411/fitgang_app/saas

# 3. Mise à jour du code
git pull

# 4. Activer environnement virtuel (si existe)
source venv/bin/activate

# 5. Créer la table blog_posts
python3 << 'EOF'
from app import create_app, db
from app.models import BlogPost

app = create_app('production')
with app.app_context():
    db.create_all()
    print("✓ Table blog_posts créée")
EOF

# 6. Redémarrer l'application
mkdir -p tmp
touch tmp/restart.txt

# 7. Vérifier
python3 << 'EOF'
from app import create_app, db
from app.models import BlogPost

app = create_app('production')
with app.app_context():
    count = BlogPost.query.count()
    print(f"✓ {count} articles dans la base")
EOF
```

---

## ✅ Vérification après déploiement

Testez ces URLs :

1. **https://fitgang.fr/blog**
   - Devrait afficher "Aucun article" (c'est normal !)
   - Grille 3 colonnes prête

2. **https://fitgang.fr/admin/blog**
   - Interface de gestion visible
   - Bouton "Nouvel Article"

3. **https://fitgang.fr/profile/photos**
   - Ne donne PLUS d'erreur 500 ✅

---

## 📝 Créer votre premier article

1. Allez sur **https://fitgang.fr/login**
2. Connectez-vous en admin
3. Menu **Admin → "Gérer Blog"**
4. Cliquez **"Nouvel Article"**
5. Remplissez :

```
Titre: Mon Premier Article FitGang
Slug: mon-premier-article-fitgang (auto-généré)
Extrait: Bienvenue sur le blog FitGang...
Catégorie: Conseils
Image principale: https://i.imgur.com/exemple.jpg
Contenu:
<h2>Bienvenue</h2>
<p>Ceci est mon premier article sur le blog FitGang!</p>
<img src="https://i.imgur.com/exemple2.jpg" alt="Image">

☑ Publier l'article
```

6. Cliquez **"Enregistrer"**
7. Allez sur **https://fitgang.fr/blog** → Votre article apparaît ! 🎉

---

## 🖼️ Où héberger les images ?

### Option 1: Imgur (Gratuit, Facile)
```
1. Allez sur https://imgur.com
2. Cliquez "New post"
3. Uploadez votre image
4. Clic droit sur l'image → "Copier l'adresse de l'image"
5. Collez l'URL dans "Image principale"
```

### Option 2: Votre serveur
```bash
# Uploadez via FTP/SSH dans:
/home/wrbh3411/fitgang_app/saas/app/static/images/blog/

# Utilisez l'URL:
https://fitgang.fr/static/images/blog/mon-image.jpg
```

---

## 🎨 Format du contenu (HTML)

```html
<!-- Titre -->
<h2>Mon Titre de Section</h2>

<!-- Paragraphe -->
<p>Mon texte avec du <strong>gras</strong></p>

<!-- Image -->
<img src="https://i.imgur.com/exemple.jpg" alt="Description">

<!-- Liste -->
<ul>
  <li>Point 1</li>
  <li>Point 2</li>
</ul>

<!-- Citation -->
<blockquote>Une citation inspirante</blockquote>
```

---

## ❓ Problèmes courants

### Erreur 500 sur /blog
```bash
cd /home/wrbh3411/fitgang_app/saas
python3 -c "from app import create_app, db; app = create_app('production'); app.app_context().push(); db.create_all()"
touch tmp/restart.txt
```

### Les images ne s'affichent pas
- ✅ Vérifiez que l'URL commence par `https://`
- ✅ Testez l'URL dans votre navigateur
- ✅ Utilisez Imgur pour plus de simplicité

### "Aucun article"
- C'est normal si vous n'avez pas encore créé d'articles !
- Allez dans `/admin/blog/add` pour créer le premier

---

## 📊 Ce qui a été corrigé

1. ✅ **Route `/blog`** : Fonctionne avec grille 3 colonnes
2. ✅ **Images** : Affichage 250x250px automatique
3. ✅ **Route `/profile/photos`** : Ne donne plus d'erreur 500
4. ✅ **Admin blog** : Interface complète de gestion
5. ✅ **Pagination** : 9 articles par page
6. ✅ **Filtres** : Par catégorie
7. ✅ **Compteur** : Nombre de vues par article

---

## 🎯 Routes disponibles

| Route | Description |
|-------|-------------|
| `/blog` | Liste des articles (grille 3x3) |
| `/blog/<slug>` | Article complet |
| `/blog?categorie=Nutrition` | Filtre par catégorie |
| `/admin/blog` | Gestion des articles |
| `/admin/blog/add` | Créer un article |
| `/admin/blog/<id>/edit` | Modifier un article |

---

## 🎉 C'est prêt !

Votre blog est maintenant opérationnel avec :
- ✅ Grille 3 cartes par ligne (responsive)
- ✅ Images 250x250px
- ✅ Interface admin complète
- ✅ Support HTML riche
- ✅ Pagination et filtres
- ✅ Compteur de vues

**Besoin d'aide ?** Voir le guide complet : `DEPLOIEMENT_BLOG.md`
