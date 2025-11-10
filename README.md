# 🏋️ FitGang - Application Web de Fitness

Application web complète développée avec Flask, SQLAlchemy et Bootstrap 5. Plateforme de vente et gestion de programmes fitness et ebooks avec système de paiement Stripe intégré.

## 🎯 Fonctionnalités

### Pour les Utilisateurs
- ✅ Inscription / Connexion sécurisée
- ✅ Profil personnalisé (poids, taille, objectifs)
- ✅ Achat de programmes fitness et ebooks via Stripe
- ✅ Bibliothèque personnelle de contenus achetés
- ✅ Suivi des progressions (séances, poids, notes)
- ✅ Téléchargement des ebooks après achat

### Pour les Administrateurs
- ✅ Dashboard avec statistiques (utilisateurs, ventes, revenus)
- ✅ CRUD complet pour les programmes fitness
- ✅ CRUD complet pour les ebooks
- ✅ Gestion des achats et suivi des ventes

## 🛠️ Stack Technique

- **Backend**: Python 3.11+ avec Flask
- **Database**: SQLAlchemy + SQLite (modifiable pour PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5 + Jinja2
- **Authentification**: Flask-Login
- **Formulaires**: Flask-WTF + WTForms
- **Paiement**: Stripe API (mode test)
- **Migrations**: Flask-Migrate

## 📦 Installation

### 1. Cloner le projet

```bash
cd fitgang_app
```

### 2. Créer un environnement virtuel

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Linux/Mac:
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de l'environnement

Créer un fichier `.env` à la racine du projet (copier depuis `.env.example`):

```bash
cp .env.example .env
```

Modifier le fichier `.env` avec vos propres valeurs:

```env
SECRET_KEY=votre-cle-secrete-aleatoire-tres-longue
STRIPE_PUBLIC_KEY=pk_test_votre_cle_publique_stripe
STRIPE_SECRET_KEY=sk_test_votre_cle_secrete_stripe
STRIPE_WEBHOOK_SECRET=whsec_votre_secret_webhook
```

**🔑 Pour obtenir vos clés Stripe:**
1. Créer un compte sur [stripe.com](https://stripe.com)
2. Aller dans "Developers" > "API keys"
3. Utiliser les clés de TEST (commençant par `pk_test_` et `sk_test_`)

### 5. Initialiser la base de données

```bash
flask init-db
```

Ou avec Python:

```bash
python run.py
# Puis Ctrl+C pour arrêter
```

La base de données SQLite `fitgang.db` sera automatiquement créée.

## 🚀 Lancement de l'application

### Méthode 1: Avec Flask CLI

```bash
flask run
```

### Méthode 2: Avec Python

```bash
python run.py
```

L'application sera accessible sur: **http://localhost:5000**

## 👤 Créer un compte administrateur

### Méthode 1: Via la commande Flask

```bash
flask create-admin
```

Suivre les instructions pour entrer:
- Email de l'admin
- Mot de passe
- Prénom

### Méthode 2: Via Flask Shell

```bash
flask shell
```

Puis dans le shell Python:

```python
from app.models import User
from app import db
from werkzeug.security import generate_password_hash

# Créer l'admin
admin = User(
    email='admin@fitgang.fr',
    password_hash=generate_password_hash('VotreMotDePasse123'),
    prenom='Admin',
    is_admin=True
)

db.session.add(admin)
db.session.commit()
print("✅ Admin créé avec succès!")
exit()
```

## 📁 Structure du Projet

```
fitgang_app/
│
├── app/
│   ├── __init__.py          # Initialisation de l'app Flask
│   ├── models.py            # Modèles SQLAlchemy (User, Programme, Ebook, etc.)
│   ├── routes.py            # Routes et vues de l'application
│   ├── forms.py             # Formulaires Flask-WTF
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # CSS personnalisé FitGang
│   │   ├── js/              # JavaScript (vide pour le moment)
│   │   └── images/          # Images et logos
│   │
│   └── templates/           # Templates Jinja2
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── profile.html
│       ├── programmes.html
│       ├── ebooks.html
│       ├── add_progression.html
│       ├── admin_dashboard.html
│       ├── admin_programmes.html
│       ├── admin_ebooks.html
│       ├── admin_programme_form.html
│       └── admin_ebook_form.html
│
├── config.py                # Configuration de l'application
├── run.py                   # Point d'entrée de l'application
├── requirements.txt         # Dépendances Python
├── .env.example            # Exemple de fichier d'environnement
├── .env                    # Variables d'environnement (à créer)
└── README.md               # Ce fichier
```

## 🗄️ Modèles de Base de Données

### User
- Email, mot de passe (hashé)
- Informations personnelles (prénom, nom, poids, taille, objectifs)
- Statut admin
- Relations: achats, progressions

### Programme
- Titre, description, contenu détaillé
- Prix, niveau (Débutant/Intermédiaire/Avancé)
- Durée, image
- Statut actif/inactif

### Ebook
- Titre, description
- Prix, image de couverture
- Lien de téléchargement
- Nombre de pages
- Statut actif/inactif

### Achat
- Utilisateur, article (programme ou ebook)
- Prix payé
- ID de session Stripe
- Date d'achat

### Progression
- Utilisateur, date
- Nom de la séance
- Poids du jour
- Exercices effectués
- Notes

## 💳 Configuration Stripe

L'application utilise **Stripe Checkout** en mode test. Voici comment configurer:

### 1. Créer un compte Stripe

Aller sur [stripe.com](https://stripe.com) et créer un compte.

### 2. Récupérer les clés API

Dans le dashboard Stripe:
- Aller dans **Developers** > **API keys**
- Copier la **Publishable key** (commence par `pk_test_`)
- Copier la **Secret key** (commence par `sk_test_`)
- Les mettre dans le fichier `.env`

### 3. Tester les paiements

Utiliser les cartes de test Stripe:
- **Succès**: `4242 4242 4242 4242`
- **Échec**: `4000 0000 0000 0002`
- Date d'expiration: n'importe quelle date future
- CVC: n'importe quel 3 chiffres

### 4. Webhooks (optionnel pour le développement)

Pour recevoir les notifications Stripe:
1. Installer Stripe CLI: [stripe.com/docs/stripe-cli](https://stripe.com/docs/stripe-cli)
2. Lancer: `stripe listen --forward-to localhost:5000/webhook`

## 🎨 Personnalisation

### Charte Graphique

Le CSS utilise une palette de couleurs FitGang:
- Fond sombre: `#0a0a0a`, `#1a1a1a`, `#2a2a2a`
- Accent rouge: `#ff4444`
- Accent orange: `#ff6b35`
- Textes: `#e0e0e0`, `#ffffff`

Pour modifier les couleurs, éditer `/app/static/css/style.css`:

```css
:root {
    --fitgang-dark: #0a0a0a;
    --fitgang-red: #ff4444;
    --fitgang-orange: #ff6b35;
    /* ... */
}
```

### Ajouter un Logo

Placer votre logo dans `/app/static/images/logo.png` et modifier le `base.html`:

```html
<a class="navbar-brand" href="/">
    <img src="{{ url_for('static', filename='images/logo.png') }}" alt="FitGang" height="40">
</a>
```

## 📊 Utilisation

### Côté Utilisateur

1. **S'inscrire** sur `/register`
2. **Se connecter** sur `/login`
3. **Parcourir** les programmes et ebooks
4. **Acheter** via Stripe Checkout
5. **Accéder** aux contenus dans le dashboard
6. **Suivre** ses progressions

### Côté Admin

1. **Se connecter** avec un compte admin
2. **Accéder** au dashboard admin
3. **Créer** des programmes et ebooks
4. **Gérer** les contenus (modifier, désactiver, supprimer)
5. **Consulter** les statistiques de ventes

## 🔒 Sécurité

- ✅ Mots de passe hashés avec Werkzeug
- ✅ Protection CSRF avec Flask-WTF
- ✅ Sessions sécurisées avec Flask-Login
- ✅ Validation des formulaires côté serveur
- ✅ Paiements sécurisés via Stripe

**⚠️ Important pour la production:**
- Utiliser une vraie clé secrète (générer avec `python -c "import secrets; print(secrets.token_hex(32))"`)
- Utiliser une base de données PostgreSQL ou MySQL
- Activer HTTPS
- Configurer les vraies clés Stripe (mode production)

## 🐛 Dépannage

### Erreur "Module not found"
```bash
pip install -r requirements.txt
```

### Erreur de base de données
```bash
# Supprimer la base existante
rm fitgang.db
# Recréer
flask init-db
```

### Port 5000 déjà utilisé
```bash
# Utiliser un autre port
flask run --port 5001
```

## 📝 Migrations de Base de Données

Pour modifier la structure de la base de données:

```bash
# Initialiser les migrations (première fois)
flask db init

# Créer une migration après modification des modèles
flask db migrate -m "Description de la modification"

# Appliquer la migration
flask db upgrade
```

## 🚀 Déploiement en Production

### Avec Gunicorn (recommandé)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

### Variables d'environnement importantes

```env
FLASK_ENV=production
SECRET_KEY=votre-vraie-cle-secrete
DATABASE_URL=postgresql://user:pass@localhost/fitgang
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
```

## 📞 Support

Pour toute question ou problème:
- Email: support@fitgang.fr
- GitHub Issues: [lien vers repo]

## 📄 Licence

© 2024 FitGang. Tous droits réservés.

---

**Développé avec ❤️ par l'équipe FitGang**

🏋️ **Prêt à transformer ton corps? Lance l'application et rejoins le gang!**
