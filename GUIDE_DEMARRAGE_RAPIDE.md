# 🎉 FITGANG EST EN LIGNE ! Guide de Démarrage Rapide

## ✅ Statut Actuel

🌐 **Site en ligne :** https://fitgang.fr
🎨 **Logo intégré :** ✅
🔧 **Configuration :** ✅
📦 **Base de données :** ✅

---

## 🔐 ÉTAPE 1 : Créer le compte administrateur

**Sur le serveur o2switch, lance :**

```bash
cd /home/wrbh3411/fitgang.fr
chmod +x create_admin_simple.sh
./create_admin_simple.sh
```

**Tu obtiendras les identifiants :**
- 📧 Email : `admin@fitgang.fr`
- 🔑 Mot de passe : `admin123`

---

## 🏋️ ÉTAPE 2 : Te connecter à l'administration

1. **Va sur :** https://fitgang.fr/login
2. **Connecte-toi avec :**
   - Email : `admin@fitgang.fr`
   - Mot de passe : `admin123`

3. **⚠️ IMPORTANT : Change le mot de passe immédiatement !**
   - Va dans **Mon Profil**
   - Change le mot de passe par défaut

---

## 🎯 ÉTAPE 3 : Ajouter du contenu

### A. Ajouter des Programmes de Fitness

1. Dans le menu admin, clique sur **Admin > Gérer Programmes**
2. Clique sur **Nouveau Programme**
3. Remplis les informations :
   - **Nom** : Ex. "Programme Prise de Masse"
   - **Description** : Décris le programme
   - **Prix** : Ex. 49.99
   - **Durée** : Ex. "8 semaines"
   - **Niveau** : Débutant / Intermédiaire / Avancé
   - **Image** : URL de l'image du programme

4. Clique sur **Créer**

### B. Ajouter des Ebooks

1. Dans le menu admin, clique sur **Admin > Gérer Ebooks**
2. Clique sur **Nouvel Ebook**
3. Remplis les informations :
   - **Titre** : Ex. "Guide Nutrition"
   - **Description** : Décris l'ebook
   - **Prix** : Ex. 19.99
   - **Auteur** : Ton nom
   - **Format** : Ex. "PDF - 120 pages"
   - **Image** : URL de la couverture

4. Clique sur **Créer**

---

## 💳 ÉTAPE 4 : Configurer Stripe pour les paiements

### Mode Test (Actuellement activé)

Ton site est en **mode TEST** avec des clés Stripe de placeholder.

**Pour tester :**
- Utilise la carte : `4242 4242 4242 4242`
- N'importe quelle date future
- N'importe quel CVC

### Passer en Mode Production

#### 1. Créer un compte Stripe

- Va sur https://stripe.com
- Crée un compte
- Complète la vérification de ton identité et compte bancaire

#### 2. Récupérer tes clés API LIVE

- Connecte-toi à Stripe
- Va dans **Developers > API keys**
- **Active le mode LIVE** (pas TEST)
- Copie :
  - `Publishable key` (commence par `pk_live_...`)
  - `Secret key` (commence par `sk_live_...`)

#### 3. Mettre à jour le fichier .env sur o2switch

```bash
# Connecte-toi en SSH
ssh wrbh3411@fitgang.fr -p 22

# Éditer le .env
cd /home/wrbh3411/fitgang.fr
nano .env
```

**Remplace :**
```env
STRIPE_PUBLIC_KEY=pk_test_VOTRE_CLE_PUBLIQUE_ICI
STRIPE_SECRET_KEY=sk_test_VOTRE_CLE_SECRETE_ICI
```

**Par tes vraies clés :**
```env
STRIPE_PUBLIC_KEY=pk_live_ta_vraie_cle_publique
STRIPE_SECRET_KEY=sk_live_ta_vraie_cle_secrete
```

**Sauvegarde :** CTRL+O, ENTER, CTRL+X

#### 4. Configurer le Webhook Stripe

1. Dans Stripe : **Developers > Webhooks**
2. Clique **Add endpoint**
3. **Endpoint URL :** `https://fitgang.fr/webhook`
4. **Événements à écouter :** Sélectionne `checkout.session.completed`
5. Clique **Add endpoint**
6. Copie le **Signing secret** (commence par `whsec_...`)

7. Ajoute dans ton .env :
```env
STRIPE_WEBHOOK_SECRET=whsec_ton_secret_ici
```

#### 5. Redémarre l'application

```bash
cd /home/wrbh3411/fitgang.fr
touch tmp/restart.txt
```

---

## 👥 ÉTAPE 5 : Gérer les utilisateurs

### Voir les utilisateurs inscrits

1. Va dans **Admin > Dashboard**
2. Tu verras le nombre d'utilisateurs, programmes, ebooks, achats

### Gérer un utilisateur

Pour le moment, tu peux :
- Voir les utilisateurs dans la base de données
- Les achats effectués
- Les progressions

---

## 📊 ÉTAPE 6 : Suivre l'activité

### Dans l'admin dashboard, tu peux voir :

- 📈 **Nombre d'utilisateurs** inscrits
- 💪 **Nombre de programmes** disponibles
- 📚 **Nombre d'ebooks** disponibles
- 💰 **Nombre d'achats** effectués

### Visualiser les achats

1. Les achats sont enregistrés dans la table `Achat`
2. Chaque achat contient :
   - L'utilisateur
   - Le programme/ebook acheté
   - Le montant
   - La date
   - L'ID de session Stripe

---

## 🔒 SÉCURITÉ

### 1. Change le mot de passe admin
✅ **À faire immédiatement après la première connexion**

### 2. Sauvegarde régulière

**Sauvegarde la base de données :**
```bash
cd /home/wrbh3411/fitgang.fr
cp fitgang.db backups/fitgang_$(date +%Y%m%d_%H%M).db
```

**Automatiser les backups (cron) :**
```bash
crontab -e
```

Ajoute :
```
0 2 * * * cp /home/wrbh3411/fitgang.fr/fitgang.db /home/wrbh3411/fitgang.fr/backups/fitgang_$(date +\%Y\%m\%d).db
```

Cela crée un backup chaque jour à 2h du matin.

### 3. SSL/HTTPS

✅ **Déjà activé par o2switch avec Let's Encrypt**

Vérifie que ton site est accessible en HTTPS : https://fitgang.fr

---

## 🎨 PERSONNALISATION

### Modifier les couleurs

Édite `/home/wrbh3411/fitgang.fr/app/static/css/style.css` :

```css
:root {
    --fitgang-dark: #0a0a0a;      /* Fond principal */
    --fitgang-red: #ff4444;       /* Accent rouge */
    --fitgang-orange: #ff6b35;    /* Accent orange */
}
```

### Modifier le logo

Le logo est actuellement chargé depuis :
```
https://blog.fitgang.fr/wp-content/uploads/2022/04/cropped-Font-Logo-white-1.jpg
```

Pour changer, édite `app/templates/base.html` ligne 22.

### Ajouter des liens réseaux sociaux

Édite le footer dans `app/templates/base.html` lignes 102-104 :

```html
<a href="https://instagram.com/ton_compte" class="text-white me-3">
    <i class="bi bi-instagram"></i>
</a>
```

---

## 🆘 SUPPORT & MAINTENANCE

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

### Diagnostic complet

```bash
cd /home/wrbh3411/fitgang.fr
./diagnostic.sh
```

### Réparation complète

```bash
cd /home/wrbh3411/fitgang.fr
./repair_all.sh
```

---

## 📈 PROCHAINES ÉTAPES RECOMMANDÉES

### Court terme (cette semaine)

- [ ] ✅ Créer le compte admin
- [ ] ✅ Changer le mot de passe admin
- [ ] 📚 Ajouter 3-5 programmes
- [ ] 📖 Ajouter 2-3 ebooks
- [ ] 💳 Configurer Stripe en mode LIVE
- [ ] 🧪 Tester un achat de bout en bout
- [ ] 📱 Ajouter les liens réseaux sociaux

### Moyen terme (ce mois)

- [ ] 🎥 Ajouter des vidéos de présentation des programmes
- [ ] 📧 Configurer l'envoi d'emails (confirmation d'achat, etc.)
- [ ] 📊 Mettre en place Google Analytics
- [ ] 🚀 Campagne de lancement
- [ ] 💬 Ajouter un système de support/contact

### Long terme

- [ ] 📱 Application mobile (Progressive Web App)
- [ ] 🎓 Système de coaching personnalisé
- [ ] 👥 Communauté / Forum
- [ ] 📹 Plateforme vidéo intégrée
- [ ] 🏆 Système de badges et récompenses

---

## 🎉 FÉLICITATIONS !

**Ton application FitGang est maintenant en ligne et fonctionnelle !** 🏋️💪

Tu peux maintenant :
- ✅ Gérer les programmes et ebooks
- ✅ Accepter des paiements via Stripe
- ✅ Suivre les progressions des utilisateurs
- ✅ Administrer ton site facilement

**Bon succès avec FitGang ! 🔥**

---

## 📞 Contacts & Ressources

- **Documentation Flask :** https://flask.palletsprojects.com/
- **Documentation Stripe :** https://stripe.com/docs
- **Support o2switch :** Chat 24/7 dans cPanel
- **Bootstrap Docs :** https://getbootstrap.com/docs/5.3/

---

**Date de déploiement :** 11 novembre 2024
**Version :** 1.0
**Python :** 3.6.15
**Flask :** 2.0.3
**Hébergement :** o2switch
