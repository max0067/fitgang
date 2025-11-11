# 🧪 Guide: Environnement de Test sur Sous-domaine

## 🎯 Objectif

Créer un environnement de test complet sur **test.fitgang.fr** ou **staging.fitgang.fr** pour tester les nouvelles fonctionnalités sans risquer de casser le site principal.

---

## 📋 Configuration sur o2switch

### Étape 1: Créer le Sous-domaine

**Via cPanel o2switch:**

1. Connecte-toi à cPanel
2. Va dans **"Sous-domaines"** ou **"Subdomains"**
3. Crée le sous-domaine:
   - **Sous-domaine:** `test` (ou `staging`)
   - **Domaine:** `fitgang.fr`
   - **Racine du document:** `/home/wrbh3411/test.fitgang.fr` (ou laisse le chemin par défaut)
4. Clique sur **"Créer"**

o2switch va automatiquement:
- ✅ Créer le répertoire `/home/wrbh3411/test.fitgang.fr`
- ✅ Configurer Apache/Nginx
- ✅ Ajouter un certificat SSL Let's Encrypt

---

### Étape 2: Copier l'Application

**Via SSH:**

```bash
# Aller dans le dossier parent
cd /home/wrbh3411

# Copier tout le site de production vers test
cp -r fitgang.fr test.fitgang.fr

# Aller dans le nouveau dossier
cd test.fitgang.fr

# Créer une nouvelle base de données SQLite pour les tests
rm fitgang.db  # Supprimer l'ancienne DB
```

---

### Étape 3: Créer le Fichier .env de Test

**Via SSH:**

```bash
cd /home/wrbh3411/test.fitgang.fr
nano .env
```

**Contenu du .env pour test:**

```bash
# Configuration FitGang - ENVIRONNEMENT DE TEST
SECRET_KEY=your_test_secret_key_here_make_it_different
DATABASE_URL=sqlite:///fitgang_test.db
BASE_URL=https://test.fitgang.fr
FLASK_ENV=development
FLASK_DEBUG=True

# Stripe TEST mode (clés de test)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_test_...

# Email (optionnel)
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_password
```

**⚠️ Important:**
- Utilise des clés Stripe de **TEST** (pas les vraies!)
- Utilise une base de données différente (`fitgang_test.db`)
- Active le mode debug (`FLASK_DEBUG=True`)

---

### Étape 4: Initialiser la Base de Données de Test

**Via SSH:**

```bash
cd /home/wrbh3411/test.fitgang.fr

# Activer l'environnement virtuel
source /home/wrbh3411/virtualenv/test.fitgang.fr/3.6/bin/activate

# Ou si le virtualenv n'existe pas encore
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
python init_db.py

# Ou si tu utilises Flask-Migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

### Étape 5: Créer un Utilisateur Admin de Test

**Via SSH:**

```bash
cd /home/wrbh3411/test.fitgang.fr
python create_admin.py
```

Ou crée un script rapide:

```python
# create_test_admin.py
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User(
        email='admin@test.com',
        prenom='Admin',
        nom='Test',
        is_admin=True
    )
    admin.set_password('test123')
    db.session.add(admin)
    db.session.commit()
    print("Admin de test créé: admin@test.com / test123")
```

Puis:
```bash
python create_test_admin.py
```

---

### Étape 6: Configurer passenger_wsgi.py

Le fichier `passenger_wsgi.py` devrait déjà être copié, mais vérifie:

```python
import sys
import os

# Ajouter le chemin de l'application
INTERP = "/home/wrbh3411/virtualenv/test.fitgang.fr/3.6/bin/python3"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
application = create_app('default')
```

---

### Étape 7: Redémarrer l'Application Test

```bash
cd /home/wrbh3411/test.fitgang.fr
mkdir -p tmp
touch tmp/restart.txt
```

---

### Étape 8: Tester

Ouvre ton navigateur et va sur:
- **https://test.fitgang.fr**

Tu devrais voir le site en version test! 🎉

---

## 🔧 Workflow de Développement

### Pour Tester une Nouvelle Fonctionnalité:

1️⃣ **Développe en local** (ou modifie directement sur test)

2️⃣ **Upload sur test.fitgang.fr** via FTP

3️⃣ **Teste sur test.fitgang.fr**
   - Teste toutes les fonctionnalités
   - Vérifie les logs: `tail -f ~/logs/test.fitgang.fr.error.log`

4️⃣ **Si tout fonctionne** → Upload sur fitgang.fr (production)

5️⃣ **Si ça plante** → Pas de problème! La production est safe! ✅

---

## 📊 Différences Production vs Test

| Aspect | Production (fitgang.fr) | Test (test.fitgang.fr) |
|--------|------------------------|------------------------|
| Base de données | `fitgang.db` | `fitgang_test.db` |
| Stripe | Clés LIVE | Clés TEST |
| Debug mode | OFF | ON |
| Données | Vraies données clients | Données de test |
| Impact si crash | ❌ Clients bloqués | ✅ Aucun impact |

---

## 🧪 Tests à Faire sur Staging

Avant de déployer en production, teste toujours:

- ✅ Page d'accueil charge
- ✅ Login fonctionne
- ✅ Dashboard admin accessible
- ✅ Création de programme
- ✅ Paiement Stripe (en mode test)
- ✅ Nouvelle fonctionnalité (analytics, etc.)
- ✅ Pas d'erreurs dans les logs

---

## 🔄 Synchroniser Production → Test

Si tu veux copier les données de production vers test:

```bash
# Copier la base de données de prod vers test
cd /home/wrbh3411
cp fitgang.fr/fitgang.db test.fitgang.fr/fitgang_test.db

# Ou copier tout le dossier
rsync -av --exclude='fitgang.db' fitgang.fr/ test.fitgang.fr/

# Redémarrer test
cd test.fitgang.fr
touch tmp/restart.txt
```

---

## 📝 Exemple: Tester le Système Analytics

```bash
# 1. Uploader les nouveaux fichiers sur test.fitgang.fr
# app/models.py (avec classe Visit)
# app/__init__.py (avec before_request)
# app/analytics.py (complet)

# 2. Créer la table visits sur test
cd /home/wrbh3411/test.fitgang.fr
sqlite3 fitgang_test.db < create_visits_table.sql

# 3. Redémarrer
touch tmp/restart.txt

# 4. Tester
curl -I https://test.fitgang.fr
# Si 200 → OK!
# Si 500 → Regarder les logs et corriger

# 5. Si tout fonctionne sur test pendant 1 jour
# → Déployer sur production
```

---

## 🆘 Logs pour Test

```bash
# Logs d'erreur
tail -f ~/logs/test.fitgang.fr.error.log

# Ou si dans un autre emplacement
tail -f ~/test.fitgang.fr/logs/error.log
```

---

## 💡 Conseils

1. **Ne JAMAIS tester directement en production**
2. **Toujours tester sur staging d'abord**
3. **Utiliser Stripe en mode TEST sur staging**
4. **Garder staging à jour avec le code de production**
5. **Tester pendant au moins 1 heure avant de déployer en prod**

---

## 🚀 Alternative: Environnement Local

Tu peux aussi tester en local sur ton PC:

```bash
# Cloner le repo
git clone https://github.com/...

# Installer les dépendances
pip install -r requirements.txt

# Lancer en local
flask run

# Tester sur http://localhost:5000
```

---

## ✅ Checklist Déploiement

Avant chaque déploiement en production:

- [ ] Testé sur staging/test.fitgang.fr
- [ ] Aucune erreur 500
- [ ] Logs propres
- [ ] Paiements testés (Stripe test mode)
- [ ] Dashboard admin fonctionne
- [ ] Pas de régression sur les fonctionnalités existantes
- [ ] Backup de production créé
- [ ] Prêt à rollback si nécessaire

---

## 📞 Support

Pour configurer le sous-domaine, tu auras besoin:
1. Accès cPanel o2switch
2. Créer le sous-domaine (2 minutes)
3. Copier les fichiers (5 minutes)
4. Tester (10 minutes)

**Total: ~20 minutes pour avoir un environnement de test complet!**

---

**Avec cet environnement de test, tu pourras tester toutes les nouvelles fonctionnalités en toute sécurité!** 🚀

Tu éviteras les crashs en production comme celui qu'on vient de corriger! 💪
