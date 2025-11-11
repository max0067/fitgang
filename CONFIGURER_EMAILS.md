# 📧 Configurer l'envoi d'emails sur FitGang

## ❌ Pourquoi les emails ne partent pas actuellement

Les emails ne partent pas car:
1. ✅ **Flask-Mail était en double** dans requirements.txt (CORRIGÉ)
2. ❌ **Variables MAIL_* manquantes** dans le .env sur le serveur
3. ❌ **Pas de mot de passe email configuré**

---

## ⚡ Solution Rapide (5 minutes)

### 1️⃣ Créer un email sur o2switch

**Via cPanel → Comptes Email:**

1. Crée un email: **admin@fitgang.fr**
2. Définis un mot de passe fort
3. Note bien le mot de passe!

**Paramètres du serveur mail o2switch:**
- **Serveur SMTP:** `mail.fitgang.fr`
- **Port:** `465` (SSL)
- **Sécurité:** SSL activé

---

### 2️⃣ Ajouter les variables dans le .env du serveur

**Via SSH ou FTP, édite le fichier `/home/wrbh3411/public_html/fitgang.fr/.env`**

Ajoute ces lignes (remplace `TON_MOT_DE_PASSE` par le vrai mot de passe):

```bash
# Configuration Email
MAIL_SERVER=mail.fitgang.fr
MAIL_PORT=465
MAIL_USE_SSL=true
MAIL_USERNAME=admin@fitgang.fr
MAIL_PASSWORD=TON_MOT_DE_PASSE
MAIL_DEFAULT_SENDER=admin@fitgang.fr
ADMIN_EMAIL=admin@fitgang.fr
```

---

### 3️⃣ Vérifier que Flask-Mail est installé

**Via SSH:**

```bash
cd /home/wrbh3411/public_html/fitgang.fr
source venv/bin/activate
pip install Flask-Mail==0.10.0
```

Si tu as un message d'erreur avec la version 0.10.0, essaie:
```bash
pip install Flask-Mail==0.9.1
```

---

### 4️⃣ Redémarrer le site

```bash
cd /home/wrbh3411/public_html/fitgang.fr
touch tmp/restart.txt
sleep 5
```

---

## ✅ Tester l'envoi d'emails

### Test 1: Via le script de test

```bash
cd /home/wrbh3411/public_html/fitgang.fr
source venv/bin/activate
python test_email.py
```

**Si ça marche:** Tu verras `✓ Email envoyé avec succès!`
**Si erreur:** Vérifie les logs pour voir le message d'erreur

---

### Test 2: Via l'interface admin

1. Va sur **https://fitgang.fr/admin/email-campaigns**
2. Clique sur **"Nouvelle Campagne"**
3. Crée une campagne test:
   - **Nom:** Test Email
   - **Sujet:** Test d'envoi
   - **Contenu HTML:** `<p>Ceci est un test</p>`
4. Clique sur **"Test"** (bouton jaune)
5. Entre ton email
6. Vérifie ta boîte mail!

---

## 🔍 Vérifier la config actuelle

**Via SSH:**

```bash
cd /home/wrbh3411/public_html/fitgang.fr
cat .env | grep MAIL
```

Tu devrais voir toutes les variables MAIL_* définies.

---

## 🆘 Debugging

### Les emails ne partent toujours pas?

**1. Vérifie les logs:**
```bash
tail -50 ~/logs/error.log | grep -i mail
```

**2. Teste la connexion SMTP:**
```bash
cd /home/wrbh3411/public_html/fitgang.fr
source venv/bin/activate
python test_email.py
```

**3. Vérifie que Flask-Mail est bien installé:**
```bash
source venv/bin/activate
pip list | grep Flask-Mail
```

Tu devrais voir: `Flask-Mail    0.10.0` (ou 0.9.1)

---

## 📋 Checklist Configuration Email

Avant de lancer une campagne:

- [ ] Email admin@fitgang.fr créé sur o2switch
- [ ] Mot de passe email défini et sécurisé
- [ ] Variables MAIL_* ajoutées dans .env
- [ ] Flask-Mail installé (`pip list | grep Flask-Mail`)
- [ ] Site redémarré (`touch tmp/restart.txt`)
- [ ] Test d'envoi réussi (`python test_email.py`)
- [ ] Email de test reçu dans la boîte mail

---

## 💡 Conseils

1. **Utilise un mot de passe fort** pour admin@fitgang.fr
2. **Ne partage JAMAIS** le mot de passe email
3. **Teste toujours** avant d'envoyer une campagne massive
4. **Limite les envois** à 50-100 emails/batch pour éviter le spam
5. **Attends 2-5 secondes** entre chaque batch (déjà configuré)

---

## 🚀 Une fois configuré

Tu pourras:
- ✅ Envoyer des emails de bienvenue automatiques
- ✅ Envoyer des confirmations d'achat
- ✅ Lancer des campagnes newsletter
- ✅ Envoyer des tests avant les campagnes

---

## 📊 Limites d'envoi o2switch

o2switch limite généralement:
- **300-500 emails/heure** (vérifie ton plan)
- Si tu dépasses → emails bloqués temporairement

**Solution si tu as beaucoup d'abonnés:**
- Configure un délai plus long entre les batches
- Envoie en plusieurs fois (matin/après-midi)
- Ou utilise un service SMTP externe (SendGrid, Mailgun)

---

**Temps de config: 5 minutes**
**Difficulté: Facile** 🟢

Une fois configuré, les emails partiront automatiquement! 🚀
