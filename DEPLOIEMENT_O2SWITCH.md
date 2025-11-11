# 🚀 Déploiement FitGang sur o2switch

Guide complet pour déployer l'application FitGang sur l'hébergement o2switch.

## ✅ Prérequis

- ✅ Compte o2switch avec accès cPanel
- ✅ Domaine configuré (ex: fitgang.fr)
- ✅ Accès SSH activé
- ✅ Python 3.6 disponible sur o2switch

## 📋 Étapes de Déploiement

### 1️⃣ Uploader les fichiers (via FTP ou SSH)

**Option A: Via FTP (FileZilla)**
1. Connecte-toi avec FileZilla à ton serveur o2switch
2. Va dans `/home/wrbh3411/fitgang.fr/`
3. Upload tous les fichiers du projet

**Option B: Via SSH + Git**
```bash
# Connexion SSH
ssh wrbh3411@fitgang.fr -p 22

# Aller dans le répertoire
cd /home/wrbh3411/

# Cloner ou créer le dossier fitgang.fr
# (les fichiers doivent être dans ce dossier)
```

### 2️⃣ Configurer Python dans cPanel

1. Va dans **cPanel** > **Setup Python App**
2. Clique sur **Create Application**
3. Configure:
   - **Python version**: 3.6
   - **Application root**: fitgang.fr
   - **Application URL**: /
   - **Application startup file**: passenger_wsgi.py
   - **Application Entry point**: application

4. Clique sur **Create**

cPanel va créer automatiquement:
- Le virtualenv dans `/home/wrbh3411/virtualenv/fitgang.fr/3.6/`
- Les configurations Passenger dans `.htaccess`

### 3️⃣ Installer les dépendances

**Connecte-toi en SSH:**
```bash
ssh wrbh3411@fitgang.fr -p 22
```

**Upload le script fix_o2switch.sh et rends-le exécutable:**
```bash
cd /home/wrbh3411/fitgang.fr
chmod +x fix_o2switch.sh
```

**Lance le script:**
```bash
./fix_o2switch.sh
```

Ce script va automatiquement:
- ✅ Activer le virtualenv cPanel
- ✅ Installer toutes les dépendances (versions compatibles Python 3.6)
- ✅ Créer le fichier .env avec une SECRET_KEY sécurisée
- ✅ Tester l'application
- ✅ Créer la base de données avec le compte admin
- ✅ Redémarrer Passenger

### 4️⃣ Tester l'application

Va sur **https://fitgang.fr** dans ton navigateur.

Tu devrais voir la page d'accueil de FitGang !

### 5️⃣ Se connecter en admin

1. Clique sur **Connexion** dans le menu
2. Email: `admin@fitgang.fr`
3. Mot de passe: `admin123`

**⚠️ IMPORTANT: Change ce mot de passe immédiatement après ta première connexion !**

## 🔧 Commandes Utiles

### Redémarrer l'application
```bash
cd /home/wrbh3411/fitgang.fr
touch tmp/restart.txt
```

### Voir les logs d'erreur
```bash
tail -f ~/logs/error.log
```

### Réinstaller les dépendances
```bash
cd /home/wrbh3411/fitgang.fr
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate
pip install -r requirements.txt
touch tmp/restart.txt
```

### Backup de la base de données
```bash
cd /home/wrbh3411/fitgang.fr
cp fitgang.db fitgang_backup_$(date +%Y%m%d).db
```

### Créer un nouveau compte admin
```bash
cd /home/wrbh3411/fitgang.fr
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate
python create_admin.py
```

## 🆘 Problèmes Fréquents

### Erreur "ModuleNotFoundError: No module named 'dotenv'"
**Solution:**
```bash
cd /home/wrbh3411/fitgang.fr
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate
pip install python-dotenv==0.19.2
touch tmp/restart.txt
```

### Erreur "Internal Server Error"
**Solution:**
1. Vérifie les logs: `tail -f ~/logs/error.log`
2. Vérifie que passenger_wsgi.py existe et est correct
3. Vérifie que .htaccess contient la config Passenger
4. Redémarre: `touch tmp/restart.txt`

### Page blanche ou erreur 500
**Solution:**
1. Vérifie que le fichier .env existe
2. Vérifie que DATABASE_URL est défini dans .env
3. Lance le script fix_o2switch.sh

### cPanel recréé passenger_wsgi.py automatiquement
**Solution:**
- C'est normal avec CloudLinux
- Remplace le fichier après chaque modification dans cPanel
- Utilise la version avec gestion d'erreurs fournie

### L'application ne charge pas après modification
**Solution:**
```bash
cd /home/wrbh3411/fitgang.fr
touch tmp/restart.txt
```

## 💳 Configuration Stripe (Production)

### Mode Test (par défaut)
L'application est configurée avec des clés Stripe de test.
Tu peux tester les paiements avec la carte: `4242 4242 4242 4242`

### Mode Live (production)
1. **Créer un compte Stripe** sur [stripe.com](https://stripe.com)
2. **Activer ton compte** (vérification bancaire)
3. **Récupérer les clés LIVE**:
   - Va dans **Developers** > **API keys**
   - Mode LIVE (pas TEST)
   - Copie `pk_live_...` (Publishable key)
   - Copie `sk_live_...` (Secret key)

4. **Éditer .env sur le serveur**:
```bash
cd /home/wrbh3411/fitgang.fr
nano .env
```

Remplace les clés test par les clés live:
```env
STRIPE_PUBLIC_KEY=pk_live_ta_vraie_cle
STRIPE_SECRET_KEY=sk_live_ta_vraie_cle
```

5. **Configurer les Webhooks**:
   - Dans Stripe: **Developers** > **Webhooks**
   - **Add endpoint**
   - URL: `https://fitgang.fr/webhook`
   - Événement: `checkout.session.completed`
   - Copie le **Signing secret**: `whsec_...`
   - Ajoute dans .env:
   ```env
   STRIPE_WEBHOOK_SECRET=whsec_ton_secret
   ```

6. **Redémarre l'application**:
```bash
touch tmp/restart.txt
```

## 🔒 Sécurité

### SSL/HTTPS
o2switch fournit automatiquement un certificat SSL Let's Encrypt.
Vérifie que ton site est accessible en HTTPS.

### Mot de passe admin
**Change le mot de passe par défaut immédiatement !**
1. Connecte-toi avec `admin@fitgang.fr` / `admin123`
2. Va dans **Mon Profil**
3. Change le mot de passe

### Fichier .env
Le fichier .env contient des informations sensibles.
- ✅ Il est protégé par .htaccess (non accessible via web)
- ✅ Ne le commite jamais sur Git
- ✅ Fais des backups réguliers

### Base de données
```bash
# Backup quotidien recommandé
cd /home/wrbh3411/fitgang.fr
cp fitgang.db backups/fitgang_$(date +%Y%m%d).db
```

## 📊 Checklist de Production

### Avant le Lancement
- [ ] Code uploadé sur o2switch
- [ ] Python App créée dans cPanel
- [ ] Script fix_o2switch.sh exécuté avec succès
- [ ] Fichier .env configuré avec SECRET_KEY unique
- [ ] Base de données créée (fitgang.db)
- [ ] Compte admin créé
- [ ] Site accessible sur https://fitgang.fr
- [ ] SSL/HTTPS activé et fonctionnel
- [ ] Mot de passe admin changé

### Pour la Production
- [ ] Clés Stripe LIVE configurées
- [ ] Webhooks Stripe configurés
- [ ] Testé un achat complet
- [ ] Créé des programmes réels
- [ ] Créé des ebooks réels
- [ ] Backup automatique configuré

## 🎨 Personnalisation

### Ajouter ton logo
```bash
# Uploader dans app/static/images/logo.png
# Éditer app/templates/base.html
```

### Modifier les couleurs
Éditer `app/static/css/style.css`:
```css
:root {
    --fitgang-dark: #0a0a0a;      /* Fond principal */
    --fitgang-red: #ff4444;       /* Accent rouge */
    --fitgang-orange: #ff6b35;    /* Accent orange */
}
```

## 📈 Maintenance

### Mises à jour
```bash
cd /home/wrbh3411/fitgang.fr
# Si tu utilises Git:
git pull

# Réinstaller les dépendances si nécessaire
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate
pip install -r requirements.txt

# Redémarrer
touch tmp/restart.txt
```

### Surveillance
```bash
# Logs en temps réel
tail -f ~/logs/error.log

# Espace disque
df -h

# Processus Python
ps aux | grep python
```

## 📞 Support

- **o2switch Support**: Chat 24/7 dans le cPanel
- **Documentation o2switch**: [faq.o2switch.fr](https://faq.o2switch.fr)
- **Documentation Stripe**: [stripe.com/docs](https://stripe.com/docs)

---

**🏋️ Ton application FitGang est prête à être déployée sur o2switch ! 💪**

Pour déployer maintenant, suis les étapes ci-dessus.
Le script `fix_o2switch.sh` automatise la plupart du travail !
