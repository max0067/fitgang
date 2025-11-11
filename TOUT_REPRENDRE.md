# 🔧 TOUT REPRENDRE - GUIDE SIMPLE

## Le problème

Tu vois "Internal Server Error" sans message détaillé.

## La solution complète

J'ai créé **2 scripts** qui vont tout diagnostiquer et tout réparer.

---

## 📋 ÉTAPE 1 : Upload les fichiers

**Upload ces fichiers sur o2switch via FTP dans `/home/wrbh3411/fitgang.fr/` :**

- ✅ `diagnostic.sh`
- ✅ `repair_all.sh`
- ✅ `passenger_wsgi.py`
- ✅ `requirements.txt`

---

## 🔍 ÉTAPE 2 : Diagnostic

**Connecte-toi en SSH:**
```bash
ssh wrbh3411@fitgang.fr -p 22
```

**Lance le diagnostic:**
```bash
cd /home/wrbh3411/fitgang.fr
chmod +x diagnostic.sh
./diagnostic.sh
```

**Ce qu'il va faire:**
- Vérifier Python et le virtualenv
- Lister tous les modules installés
- Vérifier tous les fichiers critiques
- Tester l'application Flask
- Afficher les logs d'erreur

**Copie-moi TOUTE la sortie du diagnostic !**

---

## 🔧 ÉTAPE 3 : Réparation complète

**Lance la réparation:**
```bash
chmod +x repair_all.sh
./repair_all.sh
```

**Ce qu'il va faire:**
1. ✅ Activer le virtualenv cPanel
2. ✅ Réinstaller TOUTES les dépendances (Python 3.6 compatible)
3. ✅ Recréer le fichier .env avec vraie SECRET_KEY
4. ✅ Recréer passenger_wsgi.py avec affichage d'erreurs
5. ✅ Vérifier/Recréer .htaccess
6. ✅ Créer la base de données + compte admin
7. ✅ Tester l'application complètement
8. ✅ Configurer les permissions
9. ✅ Redémarrer Passenger

Le script va te dire exactement où ça bloque si il y a un problème.

---

## 🌐 ÉTAPE 4 : Tester

**Va sur:** https://fitgang.fr

**Tu devrais voir:**
- ✅ Page d'accueil FitGang (design dark)
- 🔧 OU une page d'erreur détaillée avec le problème exact

---

## 🆘 Si ça ne marche toujours pas

### Option A : Vérifier les logs Apache
```bash
tail -f ~/logs/error.log
```

### Option B : Redémarrer manuellement dans cPanel
1. Va dans **cPanel**
2. **Setup Python App**
3. Clique sur **Restart** à côté de ton application
4. Teste https://fitgang.fr

### Option C : Tester Passenger directement
```bash
cd /home/wrbh3411/fitgang.fr
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate
python passenger_wsgi.py
```

---

## 📝 Ce qu'on a corrigé

| Problème | Solution |
|----------|----------|
| ModuleNotFoundError dotenv | ✅ Réinstallation python-dotenv |
| DATABASE_URI None | ✅ Recréation .env correct |
| SECRET_KEY placeholder | ✅ Génération clé sécurisée |
| Flask 3.0 incompatible | ✅ Downgrade Flask 2.0.3 |
| Pas de message d'erreur | ✅ passenger_wsgi.py avec affichage détaillé |

---

## 🔑 Identifiants après réparation

```
Email: admin@fitgang.fr
Mot de passe: admin123
```

⚠️ **CHANGE CE MOT DE PASSE immédiatement après connexion !**

---

## 💡 Pourquoi "Internal Server Error" ?

Plusieurs causes possibles:
1. ❌ Modules Python manquants dans le virtualenv
2. ❌ .env mal configuré
3. ❌ passenger_wsgi.py ne gère pas les erreurs
4. ❌ Permissions incorrectes
5. ❌ Problème dans le code Python (syntaxe, imports)
6. ❌ Base de données non créée

**Le script `repair_all.sh` corrige TOUS ces problèmes !**

---

## 📞 Après avoir lancé les scripts

**Envoie-moi:**
1. La sortie complète de `./diagnostic.sh`
2. La sortie complète de `./repair_all.sh`
3. Ce que tu vois sur https://fitgang.fr

Comme ça je pourrai voir exactement où ça bloque.

---

**🏋️ On va y arriver ! Lance les 2 scripts et envoie-moi les résultats ! 💪**
