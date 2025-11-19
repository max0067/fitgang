# 📝 Déploiement du Blog FitGang

## ✅ Ce qui a été ajouté

### Modèle de données
- **BlogPost** : Articles avec titre, slug, contenu HTML, extrait, image, catégorie, tags, vues, statut publication

### Pages publiques
- **`/blog`** : Liste des articles en grille 3x3 (responsive)
  - Pagination automatique (9 articles par page)
  - Filtre par catégorie
  - Compteur de vues
  - Images 250x250px

- **`/blog/<slug>`** : Page article complet
  - Contenu HTML riche
  - Articles similaires dans sidebar
  - Boutons partage réseaux sociaux
  - Breadcrumb navigation

### Interface admin
- **`/admin/blog`** : Gestion des articles
  - Liste avec aperçu image, catégorie, statut
  - Statistiques (vues, date publication)
  - Filtres et recherche

- **`/admin/blog/add`** : Créer un article
  - Éditeur HTML
  - Auto-génération slug depuis titre
  - Prévisualisation image en temps réel
  - Choix catégorie et tags
  - Publication immédiate ou brouillon

### Corrections incluses
- ✅ Route `/profile/photos` (redirection vers `/photos`)
- ✅ Affichage images blog en grille 3 colonnes
- ✅ Système complet de gestion de contenu

---

## 🚀 Déploiement sur votre serveur

### Option 1: Script automatique (RECOMMANDÉ)

```bash
cd /home/votre_user/public_html  # ou saas/
chmod +x deploy_blog.sh
./deploy_blog.sh
```

Le script fait automatiquement:
1. Pull des modifications Git
2. Installation dépendances
3. Migration base de données
4. Redémarrage application
5. Vérification

### Option 2: Déploiement manuel

```bash
# 1. Récupérer le code
git fetch origin
git pull origin claude/fix-blog-layout-cache-01BREgfFyut2YeX3GdQanxWK
# OU simplement
git pull

# 2. Activer environnement virtuel
source venv/bin/activate

# 3. Créer la table blog_posts
python3 << 'EOF'
from app import create_app, db
from app.models import BlogPost

app = create_app('production')
with app.app_context():
    db.create_all()
    print("✓ Table blog_posts créée")
EOF

# 4. Redémarrer l'application
mkdir -p tmp
touch tmp/restart.txt

echo "✅ Déploiement terminé!"
```

---

## 📝 Créer votre premier article

1. **Connectez-vous en admin** : https://fitgang.fr/login

2. **Allez dans le menu Admin** → "Gérer Blog"

3. **Cliquez sur "Nouvel Article"**

4. **Remplissez le formulaire** :
   ```
   Titre: 10 Conseils pour une Sèche Réussie
   Slug: 10-conseils-seche-reussie (auto-généré)
   Extrait: Découvre mes 10 meilleurs conseils...
   Contenu: <h2>1. Déficit calorique</h2><p>...</p>
   Image: https://exemple.com/image-seche.jpg
   Catégorie: Nutrition
   Tags: sèche, nutrition, calories
   ✅ Publier l'article
   ```

5. **Enregistrez** → L'article sera visible sur `/blog`!

---

## 🎨 Format du contenu (HTML)

Le champ "Contenu" supporte le HTML. Exemples:

```html
<!-- Titre de section -->
<h2>Mon titre de section</h2>

<!-- Paragraphe -->
<p>Mon texte avec du <strong>gras</strong> et de l'<em>italique</em>.</p>

<!-- Liste -->
<ul>
  <li>Premier point</li>
  <li>Deuxième point</li>
</ul>

<!-- Image dans l'article -->
<img src="https://exemple.com/image.jpg" alt="Description">

<!-- Citation -->
<blockquote>Une citation inspirante</blockquote>

<!-- Lien -->
<a href="https://fitgang.fr">Lien vers FitGang</a>
```

---

## 🖼️ Affichage des images

### Grille d'articles (`/blog`)
- 3 cartes par ligne (desktop)
- 2 cartes par ligne (tablette)
- 1 carte par ligne (mobile)
- Images: 250x250px (crop automatique `object-fit: cover`)

### Page article (`/blog/<slug>`)
- Image principale: largeur 100%, hauteur max 500px
- Images dans contenu: largeur 100% automatique, responsive

### Où héberger les images ?

**Option 1: Imgur (Gratuit)**
```
1. Allez sur https://imgur.com
2. Upload votre image
3. Clic droit → Copier l'adresse de l'image
4. Collez l'URL dans le champ "Image principale"
```

**Option 2: Votre serveur**
```
1. Uploadez l'image dans app/static/images/blog/
2. URL: https://fitgang.fr/static/images/blog/mon-image.jpg
```

---

## ❓ Dépannage

### Le blog affiche "Aucun article"
- C'est normal si vous n'avez pas encore créé d'articles
- Allez dans `/admin/blog/add` pour créer le premier

### Erreur 500 sur `/blog`
```bash
# Vérifiez que la table existe
python3 << 'EOF'
from app import create_app, db
app = create_app('production')
with app.app_context():
    db.create_all()
EOF

# Redémarrez
touch tmp/restart.txt
```

### Les images ne s'affichent pas
- Vérifiez que l'URL est complète (`https://...`)
- Vérifiez que l'image est accessible publiquement
- Testez l'URL dans votre navigateur

### Le slug est invalide
- Le slug doit être URL-friendly : `mon-article-123`
- Pas d'espaces, caractères spéciaux, majuscules
- S'auto-génère depuis le titre

---

## 📊 Statistiques

Chaque article suit automatiquement:
- **Nombre de vues** : Incrémenté à chaque visite
- **Date de création**
- **Date de publication**
- **Date de modification**

Visible dans `/admin/blog`

---

## 🔗 Routes complètes

| Route | Description | Accès |
|-------|-------------|-------|
| `/blog` | Liste des articles | Public |
| `/blog/<slug>` | Article détail | Public |
| `/blog?categorie=Nutrition` | Filtre par catégorie | Public |
| `/blog?page=2` | Pagination | Public |
| `/admin/blog` | Gestion articles | Admin |
| `/admin/blog/add` | Créer article | Admin |
| `/admin/blog/<id>/edit` | Modifier article | Admin |
| `/profile/photos` | Photos profil | Utilisateur |

---

## ✅ Vérification

Après déploiement, testez:

1. ✅ `/blog` s'affiche (même vide)
2. ✅ `/admin/blog` accessible en admin
3. ✅ Créer un article de test
4. ✅ L'article apparaît sur `/blog`
5. ✅ L'image s'affiche correctement (250x250px)
6. ✅ Le détail de l'article fonctionne
7. ✅ `/profile/photos` ne donne plus d'erreur 500

---

## 🎉 C'est prêt!

Votre blog est maintenant opérationnel avec:
- ✅ Affichage 3 cartes par ligne avec images
- ✅ Interface admin complète
- ✅ Pagination et filtres
- ✅ Compteur de vues
- ✅ Support HTML riche
- ✅ Publication/brouillon
- ✅ Catégories et tags

**Besoin d'aide?** Ouvrez une issue sur GitHub ou contactez le support.
