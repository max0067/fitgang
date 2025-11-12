# 🚀 Fix Rapide - Blog sur test.fitgang.fr

## Commandes à Exécuter sur le Serveur

### 1️⃣ Se connecter et aller dans le bon dossier
```bash
cd /home/wrbh3411/test.fitgang.fr
```

### 2️⃣ Récupérer les nouveaux fichiers depuis GitHub
```bash
git pull origin claude/fix-email-campaigns-011CV29exAWnnTfzcJ4vZoRk
```

### 3️⃣ Exécuter le script de réparation
```bash
chmod +x fix_test_blog_complete.sh
./fix_test_blog_complete.sh
```

### 4️⃣ Attendre 15 secondes puis tester
```bash
sleep 15
curl -I https://test.fitgang.fr/blog
```

---

## ✅ Résultat Attendu

Si tout fonctionne, tu verras :
- `HTTP/2 200` pour /blog
- Le message "✅ ✅ ✅ NOUVEAU HEADER DÉTECTÉ! ✅ ✅ ✅"
- Nombre de dropdowns > 0

---

## 🔧 Si le Cache Persiste

```bash
cd /home/wrbh3411/test.fitgang.fr
rm -rf tmp/*
mkdir -p tmp
touch passenger_wsgi.py
echo "$(date)" > tmp/restart.txt
sleep 15
```

---

## 📱 Test dans le Navigateur

Ouvre : https://test.fitgang.fr

Tu devrais voir :
- ✅ Menu avec dropdowns (Ebooks, Compléments, Mon Profil)
- ✅ Lien "Blog" dans la navigation
- ✅ Page /blog accessible (vide pour l'instant)

---

## 🆘 En Cas de Problème

### Vérifier les fichiers
```bash
cd /home/wrbh3411/test.fitgang.fr
grep -c "class BlogPost" app/models.py       # Doit retourner 1
grep -c "TEMPLATES_AUTO_RELOAD" config.py    # Doit retourner 1
grep -c "dropdown" app/templates/base.html   # Doit retourner 37
```

### Vérifier la base de données
```bash
sqlite3 fitgang.db "SELECT name FROM sqlite_master WHERE type='table' AND name='blog_posts';"
# Doit afficher : blog_posts
```

### Voir les erreurs
```bash
tail -50 ~/logs/error.log
```
