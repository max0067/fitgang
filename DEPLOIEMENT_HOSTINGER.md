# 🚀 Déploiement de FitGang sur Hostinger

Guide complet pour déployer ton application Flask FitGang sur Hostinger.

## 📋 Prérequis

1. Un compte Hostinger (Premium ou Business pour Python)
2. Un nom de domaine (ex: fitgang.fr)
3. Accès SSH (disponible avec les plans Premium et Business)

## 🎯 Méthode 1 : Déploiement via SSH (Recommandé)

### Étape 1 : Se connecter à Hostinger via SSH

1. **Obtenir tes identifiants SSH** :
   - Connecte-toi à ton compte Hostinger
   - Va dans **Hébergement** > **Configuration avancée**
   - Cherche la section **SSH Access**
   - Note ton **hostname**, **username**, et **port**

2. **Se connecter depuis ton terminal** :
```bash
ssh username@hostname -p port
```

Exemple :
```bash
ssh u123456789@srv1.hostinger.com -p 65002
```

### Étape 2 : Préparer l'environnement Hostinger

```bash
# Vérifier la version de Python
python3 --version

# Installer pip si nécessaire
python3 -m ensurepip --upgrade

# Créer le dossier pour l'application
cd ~/domains/fitgang.fr/public_html
# OU
cd ~/public_html  # selon la structure de ton compte
```

### Étape 3 : Uploader ton application

**Option A : Via Git (Recommandé)**

```bash
# Cloner ton repository
git clone https://github.com/ton-username/fitgang.git .

# Ou si tu as déjà poussé sur GitHub
git pull origin main
```

**Option B : Via FTP/SFTP**

1. Utilise FileZilla ou un client FTP
2. Connecte-toi avec tes identifiants SFTP
3. Upload tous les fichiers du projet dans `public_html` ou ton dossier de domaine

**Option C : Via SCP depuis ton serveur actuel**

```bash
# Depuis ton serveur actuel
scp -P 65002 -r /home/wrbh3411/fitgang.fr/* username@srv1.hostinger.com:~/public_html/
```

### Étape 4 : Installer l'environnement virtuel

```bash
# Se connecter en SSH à Hostinger
cd ~/public_html  # ou ton dossier

# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Étape 5 : Configurer les variables d'environnement

```bash
# Créer le fichier .env
nano .env
```

Copie et modifie :
```env
SECRET_KEY=ta-cle-secrete-super-longue-et-aleatoire
DATABASE_URL=sqlite:///fitgang.db
STRIPE_PUBLIC_KEY=pk_live_ta_vraie_cle_publique
STRIPE_SECRET_KEY=sk_live_ta_vraie_cle_secrete
STRIPE_WEBHOOK_SECRET=whsec_ton_secret_webhook
BASE_URL=https://fitgang.fr
FLASK_ENV=production
```

**⚠️ Important** : Utilise les clés Stripe **LIVE** (pk_live_ et sk_live_) pour la production !

### Étape 6 : Initialiser la base de données

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Créer la base de données
python create_admin.py
```

### Étape 7 : Configurer Passenger (serveur WSGI de Hostinger)

Hostinger utilise Passenger pour servir les applications Python. Crée le fichier `passenger_wsgi.py` :

```bash
nano passenger_wsgi.py
```

Contenu :
```python
import sys
import os

# Ajouter le chemin de l'application
INTERP = os.path.join(os.environ['HOME'], 'public_html', 'venv', 'bin', 'python3')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Ajouter le dossier de l'application au path
sys.path.append(os.getcwd())

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Importer l'application Flask
from app import create_app

application = create_app('production')
```

### Étape 8 : Créer le fichier .htaccess

```bash
nano .htaccess
```

Contenu :
```apache
PassengerEnabled On
PassengerAppRoot /home/username/public_html
PassengerBaseURI /
PassengerPython /home/username/public_html/venv/bin/python3

<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^(.*)$ passenger_wsgi.py [L]
</IfModule>
```

**⚠️ Remplace** `username` par ton vrai username Hostinger !

### Étape 9 : Configurer les permissions

```bash
chmod 755 passenger_wsgi.py
chmod 755 run.py
chmod 644 .htaccess
```

### Étape 10 : Redémarrer l'application

```bash
# Créer un fichier restart.txt pour redémarrer Passenger
mkdir -p tmp
touch tmp/restart.txt
```

Chaque fois que tu veux redémarrer :
```bash
touch tmp/restart.txt
```

## 🎯 Méthode 2 : Via le Panel Hostinger (Plus simple)

### Étape 1 : Activer Python dans le Panel

1. Connecte-toi à ton panel Hostinger
2. Va dans **Hébergement** > **Configuration avancée**
3. Cherche **Python** ou **Application Setup**
4. Active Python pour ton domaine

### Étape 2 : Configurer l'application via le panel

1. Dans le panel, va dans **Python App Setup**
2. Configure :
   - **Python version** : 3.11 (ou la plus récente disponible)
   - **Application root** : `/public_html`
   - **Application URL** : `/` (pour la racine du domaine)
   - **Application startup file** : `passenger_wsgi.py`
   - **Application Entry point** : `application`

### Étape 3 : Upload les fichiers

1. Utilise le **File Manager** de Hostinger
2. Upload tous tes fichiers dans le dossier configuré
3. OU utilise FTP/SFTP

### Étape 4 : Installer les dépendances

Dans le terminal SSH ou via le panel :
```bash
cd ~/public_html
source venv/bin/activate
pip install -r requirements.txt
```

## 🗄️ Option : Utiliser MySQL au lieu de SQLite

Pour une meilleure performance en production :

### 1. Créer une base de données MySQL dans Hostinger

1. Va dans **Bases de données** > **MySQL**
2. Crée une nouvelle base de données
3. Note le **nom de la base**, **username**, **password**, et **hostname**

### 2. Modifier requirements.txt

Ajoute :
```
PyMySQL==1.1.0
cryptography==41.0.7
```

### 3. Modifier config.py

Remplace la ligne DATABASE_URL par :
```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'mysql+pymysql://username:password@localhost/database_name'
```

### 4. Modifier .env

```env
DATABASE_URL=mysql+pymysql://username:password@localhost/database_name
```

### 5. Réinstaller et migrer

```bash
pip install -r requirements.txt
python create_admin.py
```

## 🔒 Configuration SSL (HTTPS)

1. Dans le panel Hostinger, va dans **SSL**
2. Active le **SSL gratuit** (Let's Encrypt)
3. Force HTTPS en modifiant `.htaccess` :

```apache
# Force HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Configuration Passenger
PassengerEnabled On
PassengerAppRoot /home/username/public_html
PassengerBaseURI /
PassengerPython /home/username/public_html/venv/bin/python3
```

## 💳 Configuration Stripe en Production

1. **Passer en mode Live** :
   - Connecte-toi à ton compte Stripe
   - Active ton compte (vérification d'identité nécessaire)
   - Va dans **Developers** > **API keys**
   - Utilise les clés **Live** (pk_live_ et sk_live_)

2. **Configurer les Webhooks** :
   - Va dans **Developers** > **Webhooks**
   - Ajoute un endpoint : `https://fitgang.fr/webhook`
   - Sélectionne les événements : `checkout.session.completed`
   - Copie le **Webhook signing secret**
   - Mets-le dans `.env` : `STRIPE_WEBHOOK_SECRET=whsec_...`

## 📊 Monitoring et Logs

### Voir les logs d'erreur

```bash
# Sur Hostinger
tail -f ~/logs/error.log
# OU
tail -f ~/public_html/logs/error.log
```

### Créer un système de logs personnalisé

Modifie `run.py` pour ajouter :
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/fitgang.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('FitGang startup')
```

## 🚀 Optimisations pour la Production

### 1. Utiliser un vrai serveur WSGI (Gunicorn)

Ajoute à `requirements.txt` :
```
gunicorn==21.2.0
```

Crée `wsgi.py` :
```python
from app import create_app

application = create_app('production')

if __name__ == "__main__":
    application.run()
```

### 2. Configurer le cache

Ajoute à `config.py` :
```python
class ProductionConfig(Config):
    # ... config existante
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 an pour les fichiers statiques
```

### 3. Compresser les fichiers statiques

Installe Flask-Compress :
```bash
pip install Flask-Compress
```

Dans `app/__init__.py` :
```python
from flask_compress import Compress

compress = Compress()

def create_app(config_name='default'):
    app = Flask(__name__)
    # ... config existante
    compress.init_app(app)
    return app
```

## 📝 Checklist de Déploiement

- [ ] Compte Hostinger avec accès SSH
- [ ] Domaine configuré et pointé vers Hostinger
- [ ] Code uploadé via Git/FTP/SCP
- [ ] Environnement virtuel créé
- [ ] Dépendances installées
- [ ] Fichier .env configuré avec les vraies clés
- [ ] Base de données initialisée
- [ ] passenger_wsgi.py créé
- [ ] .htaccess configuré
- [ ] Permissions définies
- [ ] SSL activé (HTTPS)
- [ ] Stripe configuré en mode LIVE
- [ ] Webhooks Stripe configurés
- [ ] Compte admin créé
- [ ] Application testée sur le domaine

## 🔧 Commandes Utiles

```bash
# Redémarrer l'application
touch tmp/restart.txt

# Voir les processus Python
ps aux | grep python

# Mettre à jour l'application
cd ~/public_html
git pull
source venv/bin/activate
pip install -r requirements.txt
touch tmp/restart.txt

# Créer un backup de la base de données
cp fitgang.db fitgang_backup_$(date +%Y%m%d).db

# Voir l'espace disque
df -h
du -sh *
```

## 🆘 Dépannage

### L'application ne démarre pas

1. Vérifie les logs : `tail -f ~/logs/error.log`
2. Vérifie les permissions : `ls -la passenger_wsgi.py`
3. Vérifie le chemin Python dans `.htaccess`
4. Redémarre : `touch tmp/restart.txt`

### Erreur 500

1. Active le mode debug temporairement (ATTENTION en production !)
2. Vérifie les logs
3. Vérifie que toutes les dépendances sont installées
4. Vérifie la configuration de la base de données

### Base de données verrouillée (SQLite)

Passe à MySQL pour éviter les problèmes de concurrence.

### Problèmes de permissions

```bash
chmod -R 755 ~/public_html
chmod 644 .env
chmod 644 fitgang.db
```

## 📞 Support

- **Documentation Hostinger** : [https://support.hostinger.com](https://support.hostinger.com)
- **Chat support Hostinger** : Disponible 24/7

---

**🏋️ Ton application FitGang sera bientôt en ligne sur https://fitgang.fr !**
