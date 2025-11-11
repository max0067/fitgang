# 🚨 DÉPANNAGE URGENCE - Site HS

## ✅ CORRECTIF APPLIQUÉ - 11 Nov 2025

Le problème était le modèle `Visit` dans models.py qui causait une erreur 500.
**Le correctif a été appliqué et poussé sur la branche.**

## Le site est complètement down? Voici comment le remettre en ligne

### OPTION 1: Mise à jour et redémarrage (RECOMMANDÉ) ✅ CORRECTIF INCLUS

```bash
cd /home/wrbh3411/fitgang.fr

# Récupérer le dernier code (CORRECTIF INCLUS - Visit model désactivé)
git fetch origin
git reset --hard origin/claude/fix-email-campaigns-011CV29exAWnnTfzcJ4vZoRk

# Redémarrer
mkdir -p tmp
touch tmp/restart.txt

# Attendre 5 secondes
sleep 5

# Tester
curl -I https://fitgang.fr
```

**Ce correctif désactive temporairement le modèle Visit qui causait l'erreur 500.**

Si ça ne marche toujours pas, passe à l'option 2.

---

### OPTION 2: Rollback vers version stable

```bash
cd /home/wrbh3411/fitgang.fr

# Revenir à un commit stable (avant analytics)
git reset --hard 13c73db

# Redémarrer
mkdir -p tmp
touch tmp/restart.txt
```

Ce commit est stable et connu pour fonctionner.

---

### OPTION 3: Diagnostic complet

```bash
cd /home/wrbh3411/fitgang.fr

# Vérifier les logs
tail -100 ~/logs/error.log

# Test Python
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate
python diagnostic.py
```

Envoie-moi la sortie des logs si ça ne fonctionne toujours pas.

---

### OPTION 4: Réinitialisation totale (dernier recours)

```bash
cd /home/wrbh3411/fitgang.fr

# Sauvegarder .env
cp .env .env.backup

# Revenir à main/master
git fetch origin
git checkout main  # ou master selon ta branche principale
git pull origin main

# Restaurer .env
cp .env.backup .env

# Redémarrer
mkdir -p tmp
touch tmp/restart.txt
```

---

## Vérifier que ça marche

```bash
# Test simple
curl https://fitgang.fr

# Devrait retourner du HTML
```

Ou ouvre dans ton navigateur: https://fitgang.fr

---

## Ce qui a causé le problème

Le système d'analytics que j'ai ajouté essayait d'accéder à une table `visits` qui n'existe pas encore.

**J'ai désactivé le système dans le dernier commit**, donc en faisant l'OPTION 1, ça devrait fonctionner.

---

## Une fois le site remis en ligne

On pourra:
1. Tester localement les nouvelles features
2. Créer la table visits proprement
3. Réactiver les analytics

**Pour l'instant, la priorité est de remettre le site en ligne.**

---

## Logs à vérifier

```bash
# Logs d'erreur Apache/Passenger
tail -100 ~/logs/error.log

# Si tu as configuré des logs Python
tail -100 ~/fitgang.fr/logs/app.log

# Status du site
curl -I https://fitgang.fr
```

---

## Contact

Si rien ne fonctionne, envoie-moi:
1. La sortie de `tail -100 ~/logs/error.log`
2. Le résultat de `python diagnostic.py`
3. Le status code de `curl -I https://fitgang.fr`
