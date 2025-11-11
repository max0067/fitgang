# 🚀 Guide de Déploiement FTP - Correctif Urgence

## ✅ Package Prêt!

Le fichier **`fitgang_correctif_urgence.zip`** est prêt à être uploadé.

---

## 📥 Étape 1: Télécharger le ZIP

Le fichier se trouve ici:
```
fitgang_correctif_urgence.zip (11 KB)
```

Télécharge-le sur ton ordinateur.

---

## 📦 Étape 2: Extraire le ZIP

Dézippe le fichier sur ton PC. Tu verras cette structure:

```
fitgang_correctif_urgence/
├── INSTRUCTIONS_DEPLOIEMENT.txt
├── DEPANNAGE_URGENCE.md
└── app/
    ├── models.py
    ├── __init__.py
    └── analytics.py
```

---

## 🌐 Étape 3: Connexion FTP

Connecte-toi à ton FTP o2switch avec tes identifiants:
- **Serveur**: ftp.ton-domaine.com (ou selon tes identifiants o2switch)
- **Utilisateur**: wrbh3411
- **Mot de passe**: [ton mot de passe FTP]

---

## 📤 Étape 4: Upload des Fichiers

### Important: Crée d'abord un backup!

**Option A: Via FTP**
Télécharge d'abord ces 3 fichiers depuis le serveur et sauvegarde-les:
- `/home/wrbh3411/fitgang.fr/app/models.py`
- `/home/wrbh3411/fitgang.fr/app/__init__.py`
- `/home/wrbh3411/fitgang.fr/app/analytics.py`

**Option B: Via SSH** (recommandé)
```bash
cd /home/wrbh3411/fitgang.fr
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz app/models.py app/__init__.py app/analytics.py
```

### Ensuite, upload les nouveaux fichiers:

Via ton client FTP (FileZilla, Cyberduck, etc.), uploade:

| Fichier local | Destination serveur |
|---------------|---------------------|
| `app/models.py` | `/home/wrbh3411/fitgang.fr/app/models.py` |
| `app/__init__.py` | `/home/wrbh3411/fitgang.fr/app/__init__.py` |
| `app/analytics.py` | `/home/wrbh3411/fitgang.fr/app/analytics.py` |
| `DEPANNAGE_URGENCE.md` | `/home/wrbh3411/fitgang.fr/DEPANNAGE_URGENCE.md` |

**⚠️ IMPORTANT**: Écrase les anciens fichiers (remplace-les)!

---

## 🔄 Étape 5: Redémarrer l'Application

Connecte-toi en SSH:

```bash
cd /home/wrbh3411/fitgang.fr
mkdir -p tmp
touch tmp/restart.txt
```

Attends 5-10 secondes.

---

## ✅ Étape 6: Vérifier que ça Marche

```bash
curl -I https://fitgang.fr
```

**Si tu vois `HTTP/2 200`** → ✅ **LE SITE EST EN LIGNE!**

**Si tu vois `HTTP/2 500`** → ❌ Envoie-moi les logs:
```bash
tail -50 ~/logs/error.log
```

---

## 🌐 Test Final dans le Navigateur

Ouvre ces URLs et vérifie qu'elles fonctionnent:

1. ✅ https://fitgang.fr
2. ✅ https://fitgang.fr/login
3. ✅ https://fitgang.fr/admin
4. ✅ https://fitgang.fr/programme/2

---

## 🎯 Ce qui a été corrigé

### app/models.py
- ❌ Classe `Visit` temporairement désactivée (commentée)
- ✅ Empêche l'erreur 500 causée par la table manquante

### app/__init__.py
- ❌ Hook `before_request` pour analytics désactivé
- ✅ Plus de tentative de tracking des visites

### app/analytics.py
- ✅ Vérification si la table `visits` existe
- ✅ Retourne des valeurs par défaut si la table n'existe pas
- ✅ Aucune erreur n'est levée

---

## 📋 Après Remise en Ligne

Une fois le site stable, on pourra:

1. ✅ Créer la table `visits` dans la base de données
2. ✅ Réactiver le modèle `Visit`
3. ✅ Réactiver le système d'analytics
4. ✅ Tester en local avant de déployer

---

## ❓ Questions Fréquentes

### Le site est toujours down après l'upload?

Vérifie:
1. Les fichiers ont bien été uploadés dans les bons dossiers
2. Tu as bien fait `touch tmp/restart.txt`
3. Attends 10 secondes et réessaye

### J'ai uploadé mais rien ne change?

```bash
# Force le redémarrage
cd /home/wrbh3411/fitgang.fr
touch tmp/restart.txt
sleep 10
curl -I https://fitgang.fr
```

### Comment restaurer le backup?

Via FTP, re-uploade les 3 fichiers que tu as sauvegardés à l'étape 4.

Ou via SSH:
```bash
cd /home/wrbh3411/fitgang.fr
tar -xzf backup_YYYYMMDD_HHMMSS.tar.gz
touch tmp/restart.txt
```

---

## 🆘 Support

Si ça ne marche toujours pas, envoie-moi:

1. ✅ `curl -I https://fitgang.fr`
2. ✅ `tail -50 ~/logs/error.log`
3. ✅ Capture d'écran de ton FTP (structure des dossiers)

---

**Temps estimé: 5-10 minutes**

Bon courage! 💪
