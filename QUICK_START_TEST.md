# ⚡ Quick Start - Environnement de Test

## 🎯 En 5 Minutes

Voici comment configurer **test.fitgang.fr** rapidement.

---

## Méthode 1: Script Automatique (Recommandé)

### Via SSH:

```bash
# 1. Upload le script sur le serveur via FTP
# setup_test_environment.sh → /home/wrbh3411/

# 2. Connecte-toi en SSH et exécute:
cd /home/wrbh3411
chmod +x setup_test_environment.sh
./setup_test_environment.sh
```

Le script va:
- ✅ Copier tout le site de prod vers test
- ✅ Créer le fichier .env de test
- ✅ Configurer passenger_wsgi.py
- ✅ Créer la structure des dossiers

**Temps: ~2 minutes**

---

## Méthode 2: Manuel

### Via SSH:

```bash
# 1. Copier le site
cd /home/wrbh3411
cp -r fitgang.fr test.fitgang.fr

# 2. Supprimer l'ancienne DB
cd test.fitgang.fr
rm fitgang.db

# 3. Créer le .env
nano .env
# (Copie le contenu du guide)

# 4. Redémarrer
mkdir -p tmp
touch tmp/restart.txt
```

**Temps: ~5 minutes**

---

## Étapes Finales (Important!)

### 1. Créer le Sous-domaine dans cPanel

**cPanel o2switch:**
- Sous-domaines → Créer
- **Sous-domaine:** `test`
- **Domaine:** `fitgang.fr`
- **Racine:** `/home/wrbh3411/test.fitgang.fr`
- Valider

**SSL sera automatiquement configuré par o2switch!**

---

### 2. Modifier le .env avec tes Clés Stripe TEST

```bash
cd /home/wrbh3411/test.fitgang.fr
nano .env
```

**Remplace:**
```
STRIPE_PUBLIC_KEY=pk_test_TON_CODE_ICI
STRIPE_SECRET_KEY=sk_test_TON_CODE_ICI
```

Tu peux trouver tes clés de test sur:
👉 https://dashboard.stripe.com/test/apikeys

---

### 3. Initialiser la Base de Données

```bash
cd /home/wrbh3411/test.fitgang.fr
python init_db.py
```

Ou si tu as déjà le script:
```bash
python create_admin.py
```

---

### 4. Tester

Ouvre ton navigateur:
👉 **https://test.fitgang.fr**

**Si ça marche:** ✅ C'est bon!
**Si erreur 500:** Regarde les logs:

```bash
tail -50 ~/logs/test.fitgang.fr.error.log
```

---

## 🧪 Tester le Système Analytics sur Test

Maintenant que tu as un environnement de test, voici comment tester les analytics:

### 1. Upload les Fichiers Analytics sur TEST

Via FTP, uploade sur **test.fitgang.fr**:
- `app/models.py` (avec classe Visit non commentée)
- `app/__init__.py` (avec before_request actif)
- `app/analytics.py` (version complète)

### 2. Créer la Table visits

```bash
cd /home/wrbh3411/test.fitgang.fr
sqlite3 fitgang_test.db < create_visits_table.sql
```

### 3. Redémarrer Test

```bash
touch tmp/restart.txt
sleep 5
curl -I https://test.fitgang.fr
```

### 4. Tester les Analytics

- Va sur https://test.fitgang.fr
- Navigue sur plusieurs pages
- Va sur https://test.fitgang.fr/admin
- Vérifie que tu vois les stats de visiteurs

**Si ça fonctionne pendant 1 jour → Déploie en prod!**
**Si ça plante → Pas grave, la prod est safe!** ✅

---

## 💡 Workflow Quotidien

```
1. Développe nouvelle feature
2. Upload sur test.fitgang.fr
3. Teste pendant quelques heures
4. Si OK → Upload sur fitgang.fr (production)
5. Si KO → Corrige sur test sans impacter la prod
```

---

## 🔄 Synchroniser Prod → Test

Pour copier les données de prod vers test:

```bash
cd /home/wrbh3411
cp fitgang.fr/fitgang.db test.fitgang.fr/fitgang_test.db
cd test.fitgang.fr
touch tmp/restart.txt
```

---

## 🆘 Logs

```bash
# Logs de test
tail -f ~/logs/test.fitgang.fr.error.log

# Logs de production
tail -f ~/logs/error.log
```

---

## ✅ Checklist

Avant de déployer en production:

- [ ] Testé sur test.fitgang.fr pendant au moins 1h
- [ ] Aucune erreur 500
- [ ] Logs propres
- [ ] Toutes les pages chargent
- [ ] Backup de prod créé

---

## 📦 Fichiers à Uploader

Tu as maintenant 2 versions des fichiers:

**Version STABLE (actuellement en prod):**
- Dans `fitgang_rollback_stable.zip`
- Sans analytics
- Fonctionne ✅

**Version avec ANALYTICS (à tester):**
- Dans le dépôt GitHub (branche actuelle)
- Avec système de tracking
- À tester sur test.fitgang.fr d'abord!

---

**Temps total de setup: 5-10 minutes**
**Bénéfice: Plus jamais de crash en production!** 🚀
