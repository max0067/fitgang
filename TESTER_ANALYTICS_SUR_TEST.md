# 🧪 Tester les Analytics sur test.fitgang.fr

## 🎯 Objectif

Tester le système d'analytics complet sur **test.fitgang.fr** avant de le déployer en production.

**⚠️ IMPORTANT:** Ce test se fait UNIQUEMENT sur test.fitgang.fr. La production reste inchangée et sécurisée!

---

## 📦 Package Prêt

**Fichier:** `fitgang_analytics_pour_test.zip` **(9.7 KB)**

**Contenu:**
- ✅ `app/models.py` - Avec classe Visit **ACTIVÉE**
- ✅ `app/__init__.py` - Avec tracking **ACTIVÉ**
- ✅ `app/analytics.py` - Version complète
- ✅ `create_visits_table.sql` - Script pour créer la table
- ✅ `DEPLOIEMENT_ANALYTICS_TEST.txt` - Instructions détaillées

---

## ⚡ DÉPLOIEMENT RAPIDE (10 minutes)

### 1️⃣ BACKUP (via SSH)

```bash
cd /home/wrbh3411/test.fitgang.fr
cp app/models.py app/models.py.backup
cp app/__init__.py app/__init__.py.backup
cp app/analytics.py app/analytics.py.backup
```

### 2️⃣ UPLOAD VIA FTP

Télécharge le ZIP, extrais-le, puis uploade ces fichiers sur **test.fitgang.fr**:

| Fichier | Destination |
|---------|-------------|
| `app/models.py` | `/home/wrbh3411/test.fitgang.fr/app/models.py` |
| `app/__init__.py` | `/home/wrbh3411/test.fitgang.fr/app/__init__.py` |
| `app/analytics.py` | `/home/wrbh3411/test.fitgang.fr/app/analytics.py` |
| `create_visits_table.sql` | `/home/wrbh3411/test.fitgang.fr/create_visits_table.sql` |

**⚠️ ÉCRASE les fichiers existants!**

### 3️⃣ CRÉER LA TABLE VISITS (via SSH)

```bash
cd /home/wrbh3411/test.fitgang.fr

# Créer la table
sqlite3 fitgang_test.db < create_visits_table.sql

# Vérifier que la table existe
sqlite3 fitgang_test.db "SELECT name FROM sqlite_master WHERE type='table' AND name='visits';"
```

Tu devrais voir: `visits`

### 4️⃣ REDÉMARRER (via SSH)

```bash
cd /home/wrbh3411/test.fitgang.fr
touch tmp/restart.txt
sleep 5
curl -Ik https://test.fitgang.fr
```

**Si tu vois `HTTP/2 200`** → ✅ Parfait!
**Si tu vois `HTTP/2 500`** → Rollback immédiat (voir ci-dessous)

---

## ✅ VÉRIFIER QUE ÇA MARCHE

### Test 1: Le site charge

Ouvre dans ton navigateur:
- https://test.fitgang.fr

Le site devrait charger normalement.

### Test 2: Le tracking fonctionne

1. Navigue sur plusieurs pages de test.fitgang.fr
2. Va sur https://test.fitgang.fr/admin
3. **Tu devrais voir les stats de visiteurs!** 📊

### Test 3: Vérifier la base de données

Via SSH:
```bash
cd /home/wrbh3411/test.fitgang.fr
sqlite3 fitgang_test.db "SELECT COUNT(*) FROM visits;"
```

Le nombre devrait être > 0 après avoir navigué.

---

## 🛑 ROLLBACK SI PROBLÈME

Si le site test plante (HTTP 500):

```bash
cd /home/wrbh3411/test.fitgang.fr

# Restaurer les backups
cp app/models.py.backup app/models.py
cp app/__init__.py.backup app/__init__.py
cp app/analytics.py.backup app/analytics.py

# Redémarrer
touch tmp/restart.txt
sleep 5

# Vérifier
curl -Ik https://test.fitgang.fr
```

---

## 📊 STATS DISPONIBLES

Dans le dashboard admin (`/admin`), tu verras:

- 👥 **Visiteurs en direct** (15 dernières minutes)
- 📈 **Visiteurs aujourd'hui / hier**
- 📅 **Visiteurs cette semaine / ce mois**
- 📄 **Pages les plus visitées**
- 🔗 **Sources de trafic**
- 📊 **Graphique tendance 7 derniers jours**

---

## 🧪 PÉRIODE DE TEST

**Avant de déployer en production:**

- ✅ Teste pendant au moins **2-3 heures** sur test.fitgang.fr
- ✅ Navigue sur toutes les pages
- ✅ Vérifie que les stats augmentent
- ✅ Vérifie qu'il n'y a pas d'erreurs dans les logs
- ✅ Vérifie que le site reste rapide

**Commande pour surveiller les logs:**
```bash
tail -f ~/logs/test.fitgang.fr.error.log
```

---

## 🚀 DÉPLOIEMENT EN PRODUCTION

**Seulement si tout fonctionne bien sur test pendant 2-3 heures!**

1. Faire un backup de production
2. Uploader les mêmes fichiers sur **fitgang.fr** (pas test!)
3. Créer la table visits sur **fitgang.db** (pas fitgang_test.db!)
4. Redémarrer fitgang.fr
5. Surveiller les logs pendant 30 minutes

**Mais pour l'instant: ON TESTE UNIQUEMENT SUR TEST!** ✅

---

## 📋 CHECKLIST

Avant de déployer en production:

- [ ] Testé sur test.fitgang.fr pendant 2-3 heures
- [ ] Aucune erreur HTTP 500
- [ ] Logs propres (pas d'erreurs Python)
- [ ] Stats de visiteurs s'affichent correctement
- [ ] Navigation fluide sur toutes les pages
- [ ] Compteur de visiteurs augmente normalement
- [ ] Backup de production créé

---

## 🏗️ ARCHITECTURE

### Après déploiement sur TEST:

```
┌─────────────────────────────────────────────────┐
│ PRODUCTION (fitgang.fr)                         │
│ Status: 🟢 EN LIGNE                             │
│ Analytics: ❌ DÉSACTIVÉS                        │
│ Impact: AUCUN                                    │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ TEST (test.fitgang.fr)                          │
│ Status: 🧪 TEST                                 │
│ Analytics: ✅ ACTIVÉS                           │
│ Impact: Zéro sur les vrais utilisateurs        │
└─────────────────────────────────────────────────┘
```

---

## 🆘 DEBUGGING

Si erreur HTTP 500 sur test:

```bash
# Voir les logs
tail -50 ~/logs/test.fitgang.fr.error.log

# Vérifier que la table existe
sqlite3 fitgang_test.db ".tables"

# Compter les visites
sqlite3 fitgang_test.db "SELECT COUNT(*) FROM visits;"
```

---

## 💡 CONSEILS

1. **Teste d'abord sur test.fitgang.fr!** Ne touche pas à la prod!
2. **Surveille les logs** pendant les tests
3. **Teste pendant au moins 2-3 heures** avant la prod
4. **Garde les backups** au cas où
5. **Documente tout problème** rencontré

---

## 📖 DOCUMENTATION COMPLÈTE

Le fichier `DEPLOIEMENT_ANALYTICS_TEST.txt` (dans le ZIP) contient toutes les instructions détaillées, les rollback procedures, et le guide complet.

---

**Temps total: 10 minutes de déploiement + 2-3 heures de tests**

**Risque: ZÉRO** - test seulement, production inchangée! 🚀

Bonne chance avec les tests! 💪
