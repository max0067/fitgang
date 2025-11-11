# 🔍 Diagnostiquer Pourquoi les Emails ne Partent Pas

## 🎯 Symptôme

Tu ne reçois pas les emails quand quelqu'un s'inscrit (ni les confirmations d'achat).

---

## ⚡ Solution Rapide (2 minutes)

### 1️⃣ Lancer le Script de Diagnostic

**Via SSH:**

```bash
cd /home/wrbh3411/public_html/fitgang.fr
source venv/bin/activate
python test_mail_config.py
```

Le script va tester:
- ✓ Variables MAIL_* dans .env
- ✓ Flask-Mail installé
- ✓ Connexion SMTP
- ✓ Envoi d'un email de test

---

## 📋 Résultats Possibles

### ✅ Cas 1: Tout est OK

```
✓ TOUT EST OK! Les emails devraient fonctionner maintenant.
```

**→ Les emails vont maintenant partir lors des inscriptions!**

---

### ❌ Cas 2: Variables manquantes

```
✗ MAIL_SERVER = None
✗ MAIL_PASSWORD = NOT SET
```

**Solution:** Ajoute les variables dans `.env` (voir `CONFIGURER_EMAILS.md`)

---

### ❌ Cas 3: Flask-Mail non installé

```
✗ ERREUR: Flask-Mail n'est pas installé!
```

**Solution:**
```bash
cd /home/wrbh3411/public_html/fitgang.fr
source venv/bin/activate
pip install Flask-Mail==0.10.0
touch tmp/restart.txt
```

---

### ❌ Cas 4: Erreur SMTP

```
✗ ERREUR lors de l'envoi: [Errno 111] Connection refused
```

**Causes possibles:**
1. Mauvais mot de passe email
2. Email admin@fitgang.fr n'existe pas
3. Serveur mail.fitgang.fr non configuré

**Solution:**
1. Vérifie que l'email existe dans cPanel → Comptes Email
2. Vérifie le mot de passe dans `.env`
3. Réessaye le script

---

## 🔍 Voir les Logs en Temps Réel

**Pour voir les erreurs lors des inscriptions:**

```bash
# Terminal 1: Surveiller les logs
tail -f ~/logs/error.log

# Terminal 2: Créer un compte test
# → Va sur fitgang.fr/register et inscris-toi
```

Tu verras maintenant les messages détaillés:
- `[INSCRIPTION] Email de bienvenue envoyé à xxx@xxx.com` ✓
- `[INSCRIPTION] ⚠️ Email de bienvenue NON envoyé - Vérifier config MAIL_*` ⚠️
- `[INSCRIPTION] ✗ ERREUR lors de l'envoi de l'email de bienvenue: ...` ❌

---

## 🧪 Tester Manuellement

**1. Test basique avec test_email.py:**
```bash
cd /home/wrbh3411/public_html/fitgang.fr
source venv/bin/activate
python test_email.py
```

**2. Test complet avec test_mail_config.py:**
```bash
python test_mail_config.py
```

**3. Test d'inscription:**
- Va sur fitgang.fr/register
- Inscris-toi avec un vrai email
- Vérifie ta boîte mail

---

## ✅ Checklist Debug

- [ ] `python test_mail_config.py` passe tous les tests
- [ ] Variables MAIL_* présentes dans `.env`
- [ ] Flask-Mail installé (`pip list | grep Flask-Mail`)
- [ ] Email admin@fitgang.fr existe dans cPanel
- [ ] Mot de passe correct dans `.env`
- [ ] Site redémarré (`touch tmp/restart.txt`)
- [ ] Logs surveillés (`tail -f ~/logs/error.log`)
- [ ] Test d'inscription effectué

---

## 💡 Améliorations Faites

J'ai amélioré le logging pour que tu voies maintenant dans les logs:

**Lors d'une inscription:**
```
[INSCRIPTION] Email de bienvenue envoyé à user@example.com
```

**Lors d'un achat:**
```
[ACHAT] Email de confirmation envoyé à user@example.com
[ACHAT] Email admin envoyé à admin@fitgang.fr
```

**En cas d'erreur:**
```
[INSCRIPTION] ✗ ERREUR lors de l'envoi de l'email de bienvenue: Connection refused
[Traceback complet]
```

---

## 🆘 Si Ça Ne Marche Toujours Pas

**Envoie-moi:**

1. **Résultat du script:**
   ```bash
   python test_mail_config.py > diagnostic.txt 2>&1
   cat diagnostic.txt
   ```

2. **Variables d'environnement email:**
   ```bash
   cat .env | grep MAIL
   ```

3. **Logs récents:**
   ```bash
   tail -50 ~/logs/error.log | grep -i mail
   ```

4. **Flask-Mail installé?**
   ```bash
   source venv/bin/activate
   pip list | grep Flask-Mail
   ```

---

## 📊 Prochaines Étapes

Une fois que les emails fonctionnent:

1. ✅ Inscriptions → email de bienvenue auto
2. ✅ Achats → email de confirmation auto
3. ✅ Campagnes newsletter → envoi en masse
4. ✅ Tests avant campagnes → bouton "Test"

---

**Temps: 2 minutes**
**Difficulté: Facile** 🟢

Le script de diagnostic va identifier le problème exact! 🔍
