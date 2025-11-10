# 🏋️ Guide de Démarrage Rapide - FitGang

## ✅ Installation Complète (Déjà fait!)

L'application est **installée et prête à utiliser** !

## 🚀 L'Application est en cours d'exécution

L'application Flask tourne actuellement et est accessible sur :
- **http://127.0.0.1:5000** (localhost)
- **http://21.0.0.70:5000** (réseau)

## 🔐 Compte Administrateur

Un compte administrateur a été créé pour toi :

```
📧 Email: admin@fitgang.fr
🔑 Mot de passe: admin123
```

**⚠️ IMPORTANT:** Change ce mot de passe après ta première connexion !

## 📝 Utilisation Rapide

### 1. Accéder à l'application

Ouvre ton navigateur et va sur : **http://127.0.0.1:5000**

### 2. Se connecter en tant qu'admin

1. Clique sur **"Connexion"** en haut à droite
2. Entre l'email : `admin@fitgang.fr`
3. Entre le mot de passe : `admin123`
4. Clique sur **"Se connecter"**

### 3. Accéder au Dashboard Admin

Une fois connecté, tu verras un menu **"Admin"** dans la navigation en haut. Clique dessus pour accéder :
- **Dashboard** : Statistiques et vue d'ensemble
- **Gérer Programmes** : Ajouter/modifier/supprimer des programmes fitness
- **Gérer Ebooks** : Ajouter/modifier/supprimer des ebooks

### 4. Créer ton premier programme

1. Va dans **Admin** > **Gérer Programmes**
2. Clique sur **"Nouveau Programme"**
3. Remplis les informations :
   - **Titre** : Ex: "Programme Mass Extreme"
   - **Description** : Description courte
   - **Contenu détaillé** : Description complète du programme
   - **Prix** : Ex: 29.99
   - **Niveau** : Débutant / Intermédiaire / Avancé
   - **Durée** : Ex: "8 semaines"
   - **Image** : URL d'une image (ex: depuis imgur.com ou ton hébergeur)
   - **Actif** : Coché pour rendre le programme visible
4. Clique sur **"Enregistrer"**

### 5. Créer ton premier ebook

1. Va dans **Admin** > **Gérer Ebooks**
2. Clique sur **"Nouveau Ebook"**
3. Remplis les informations :
   - **Titre** : Ex: "Guide Complet de la Nutrition"
   - **Description** : Description complète
   - **Prix** : Ex: 19.99
   - **Image** : URL de la couverture
   - **Lien de téléchargement** : Lien Google Drive, Dropbox, etc.
   - **Nombre de pages** : Ex: 150
   - **Actif** : Coché pour rendre l'ebook visible
4. Clique sur **"Enregistrer"**

## 💳 Configuration Stripe (Pour les Paiements)

Pour activer les paiements réels avec Stripe :

### 1. Créer un compte Stripe

- Va sur [stripe.com](https://stripe.com)
- Crée un compte gratuit

### 2. Récupérer les clés API

- Dans le dashboard Stripe, va dans **Developers** > **API keys**
- Tu verras deux clés :
  - **Publishable key** (commence par `pk_test_...`)
  - **Secret key** (commence par `sk_test_...`)

### 3. Configurer l'application

Édite le fichier `.env` dans le dossier `fitgang.fr` :

```bash
nano .env
```

Remplace ces lignes :
```env
STRIPE_PUBLIC_KEY=pk_test_ta_vraie_cle_publique
STRIPE_SECRET_KEY=sk_test_ta_vraie_cle_secrete
```

Sauvegarde (Ctrl+O, Entrée, Ctrl+X)

### 4. Redémarrer l'application

Pour que les changements prennent effet, redémarre l'application (voir section "Gérer l'Application" ci-dessous).

### 5. Tester les paiements

Utilise la carte de test Stripe :
- **Numéro** : `4242 4242 4242 4242`
- **Date d'expiration** : N'importe quelle date future
- **CVC** : N'importe quel 3 chiffres
- **Code postal** : N'importe quel code

## 🎨 Personnalisation

### Ajouter ton Logo

1. Place ton logo dans le dossier : `app/static/images/`
2. Édite le fichier : `app/templates/base.html`
3. Remplace la ligne 25-26 avec :
   ```html
   <a class="navbar-brand" href="/">
       <img src="{{ url_for('static', filename='images/ton-logo.png') }}" alt="FitGang" height="40">
   </a>
   ```

### Modifier les Couleurs

Édite le fichier : `app/static/css/style.css`

Change les variables CSS au début du fichier :
```css
:root {
    --fitgang-dark: #0a0a0a;
    --fitgang-red: #ff4444;
    --fitgang-orange: #ff6b35;
    /* Modifie ces valeurs */
}
```

## 🔧 Gérer l'Application

### Voir si l'application tourne

```bash
ps aux | grep python | grep run.py
```

### Arrêter l'application

```bash
pkill -f "python run.py"
```

### Démarrer l'application

```bash
cd /home/wrbh3411/fitgang.fr
source venv/bin/activate
python run.py &
```

L'application tournera en arrière-plan.

### Voir les logs en temps réel

```bash
tail -f nohup.out
```

## 📂 Structure des Fichiers

```
fitgang.fr/
├── app/                    # Code de l'application
│   ├── __init__.py        # Initialisation Flask
│   ├── models.py          # Modèles de base de données
│   ├── routes.py          # Routes et logique
│   ├── forms.py           # Formulaires
│   ├── static/            # Fichiers statiques (CSS, JS, images)
│   └── templates/         # Templates HTML
├── venv/                  # Environnement virtuel Python
├── config.py              # Configuration
├── run.py                 # Point d'entrée
├── requirements.txt       # Dépendances
├── .env                   # Variables d'environnement
├── fitgang.db            # Base de données SQLite
└── README.md             # Documentation complète
```

## 🆘 Problèmes Courants

### L'application ne démarre pas

```bash
cd /home/wrbh3411/fitgang.fr
source venv/bin/activate
python run.py
```

Regarde les erreurs affichées.

### Erreur de base de données

Supprime et recrée la base de données :
```bash
rm fitgang.db
python create_admin.py
```

### Port 5000 déjà utilisé

Édite `run.py` et change le port :
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 🎯 Prochaines Étapes

1. ✅ **Se connecter** en tant qu'admin
2. ✅ **Créer** tes premiers programmes et ebooks
3. ✅ **Configurer** Stripe avec tes vraies clés
4. ✅ **Tester** un achat avec la carte de test
5. ✅ **Personnaliser** avec ton logo et tes couleurs
6. ✅ **Créer** des utilisateurs de test
7. ✅ **Partager** l'URL avec tes clients !

## 📞 Aide

Pour la documentation complète, consulte le fichier `README.md`.

---

**🏋️ Prêt à transformer des vies avec FitGang!**
