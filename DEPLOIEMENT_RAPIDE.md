# ⚡ Déploiement Rapide sur Hostinger

Guide ultra-rapide pour mettre FitGang en ligne sur Hostinger en 10 minutes.

## 🎯 Prérequis

- ✅ Compte Hostinger Premium ou Business (avec accès SSH)
- ✅ Domaine configuré (ex: fitgang.fr)
- ✅ Accès SSH activé dans le panel Hostinger

## 📋 Étapes Rapides

### 1️⃣ Obtenir les infos SSH (2 min)

1. Connecte-toi à **hpanel.hostinger.com**
2. Va dans **Hébergement** > ton site
3. Section **Advanced** > **SSH Access**
4. Note ces infos :
   - **Hostname** : ex: `srv1.hostinger.com`
   - **Username** : ex: `u123456789`
   - **Port** : ex: `65002`

### 2️⃣ Se connecter au serveur (1 min)

```bash
ssh u123456789@srv1.hostinger.com -p 65002
```

Entre ton mot de passe Hostinger.

### 3️⃣ Cloner le projet (1 min)

```bash
cd ~/public_html
# Supprimer les fichiers par défaut de Hostinger
rm -rf *

# Cloner ton projet (si sur GitHub)
git clone https://github.com/ton-username/fitgang.git .

# OU télécharger depuis ton serveur actuel
# (depuis une autre fenêtre terminal locale)
scp -P 65002 -r /home/wrbh3411/fitgang.fr/* u123456789@srv1.hostinger.com:~/public_html/
```

### 4️⃣ Installer Python et les dépendances (3 min)

```bash
cd ~/public_html

# Créer l'environnement virtuel
python3 -m virtualenv venv

# Activer l'environnement
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 5️⃣ Configurer l'environnement (2 min)

```bash
# Copier le fichier de config
cp production.env.example .env

# Éditer avec nano
nano .env
```

**Modifie ces valeurs importantes:**
```env
SECRET_KEY=GENERER_UNE_NOUVELLE_CLE  # python -c "import secrets; print(secrets.token_hex(32))"
STRIPE_PUBLIC_KEY=pk_live_ta_vraie_cle
STRIPE_SECRET_KEY=sk_live_ta_vraie_cle
BASE_URL=https://ton-domaine.fr
```

Sauvegarder : `Ctrl+O`, `Entrée`, `Ctrl+X`

### 6️⃣ Configurer passenger_wsgi.py (1 min)

```bash
# Éditer le fichier
nano passenger_wsgi.py
```

Remplace la ligne avec `username` par ton vrai username:
```python
INTERP = os.path.join(os.environ['HOME'], 'public_html', 'venv', 'bin', 'python3')
```

Si ton chemin est différent, ajuste-le. Exemple:
```python
INTERP = '/home/u123456789/public_html/venv/bin/python3'
```

### 7️⃣ Configurer .htaccess (1 min)

```bash
nano .htaccess
```

Remplace **TOUS** les `username` par ton vrai username Hostinger:
```apache
PassengerAppRoot /home/u123456789/public_html
PassengerPython /home/u123456789/public_html/venv/bin/python3
```

### 8️⃣ Créer la base de données (1 min)

```bash
source venv/bin/activate
python create_admin.py
```

Tu verras:
```
✅ Compte administrateur créé avec succès!
📧 Email: admin@fitgang.fr
🔑 Mot de passe: admin123
```

### 9️⃣ Configurer les permissions (30 sec)

```bash
chmod 755 passenger_wsgi.py
chmod 644 .htaccess
chmod 644 fitgang.db
```

### 🔟 Démarrer l'application (30 sec)

```bash
mkdir -p tmp
touch tmp/restart.txt
```

## 🎉 C'EST EN LIGNE !

Va sur **https://ton-domaine.fr** (remplace par ton vrai domaine).

Tu devrais voir ta page d'accueil FitGang !

## 🔐 Se connecter en Admin

1. Clique sur **Connexion**
2. Email: `admin@fitgang.fr`
3. Mot de passe: `admin123`
4. **Change le mot de passe** dans Mon Profil !

## 🔒 Activer HTTPS (SSL)

Dans le panel Hostinger:
1. Va dans **SSL**
2. Active **SSL gratuit** (Let's Encrypt)
3. Attends 5-10 minutes pour l'activation
4. Force HTTPS est déjà configuré dans `.htaccess`

## 💳 Configurer Stripe en LIVE

1. Va sur [stripe.com](https://stripe.com)
2. Active ton compte (vérification bancaire)
3. Dans **Developers** > **API keys**
4. Copie les clés **LIVE** (pk_live_ et sk_live_)
5. Mets-les dans `.env` sur le serveur
6. Redémarre: `touch tmp/restart.txt`

### Configurer les Webhooks Stripe

1. Dans Stripe: **Developers** > **Webhooks**
2. **Add endpoint**
3. URL: `https://ton-domaine.fr/webhook`
4. Événements: Sélectionne `checkout.session.completed`
5. Copie le **Signing secret**
6. Mets-le dans `.env`: `STRIPE_WEBHOOK_SECRET=whsec_...`
7. Redémarre: `touch tmp/restart.txt`

## 🔄 Redémarrer l'application

À chaque modification, redémarre:
```bash
cd ~/public_html
touch tmp/restart.txt
```

## 📝 Commandes Utiles

```bash
# Voir les logs d'erreurs
tail -f ~/logs/error.log

# Mettre à jour le code
cd ~/public_html
git pull
source venv/bin/activate
pip install -r requirements.txt
touch tmp/restart.txt

# Backup de la base de données
cp fitgang.db fitgang_backup_$(date +%Y%m%d).db

# Voir l'espace disque
df -h
```

## 🆘 Problèmes ?

### Erreur 500
```bash
# Vérifier les logs
tail -n 50 ~/logs/error.log

# Vérifier les permissions
ls -la passenger_wsgi.py

# Redémarrer
touch tmp/restart.txt
```

### L'application ne charge pas
```bash
# Vérifier que le virtualenv est correct
which python3
ls -la venv/bin/python3

# Réinstaller les dépendances
source venv/bin/activate
pip install --force-reinstall -r requirements.txt
```

### Page blanche
- Vérifie que le domaine pointe bien vers Hostinger (DNS)
- Vérifie que les fichiers sont dans `public_html`
- Vérifie `.htaccess` et `passenger_wsgi.py`

## 📞 Support

- **Hostinger Chat** : Disponible 24/7 dans le panel
- **Documentation** : support.hostinger.com

---

## 🎯 Checklist Complète

- [ ] Connecté en SSH à Hostinger
- [ ] Code uploadé dans `~/public_html`
- [ ] Environnement virtuel créé
- [ ] Dépendances installées
- [ ] Fichier `.env` configuré
- [ ] `passenger_wsgi.py` avec le bon username
- [ ] `.htaccess` avec le bon username
- [ ] Base de données créée (compte admin)
- [ ] Permissions configurées
- [ ] Application démarrée (`touch tmp/restart.txt`)
- [ ] SSL activé dans le panel Hostinger
- [ ] Clés Stripe LIVE configurées
- [ ] Webhooks Stripe configurés
- [ ] Testé un achat sur le site
- [ ] Mot de passe admin changé

---

**🏋️ Ton application FitGang est en ligne ! Félicitations ! 🎉**

Pour toute mise à jour future, utilise le script:
```bash
./deploy_hostinger.sh
```
