# Guide de déploiement complet - FitGang

## Situation actuelle

Le site fonctionne mais certaines nouvelles fonctionnalités ne sont pas encore activées sur le serveur de production car tous les fichiers ne sont pas synchronisés.

## Fonctionnalités ajoutées dans cette branche

1. ✅ **Fix email campaigns page** - Page campagne email en pleine largeur
2. ✅ **Fix images programmes** - Toutes les images ont la même taille (300px)
3. ✅ **Dashboard admin en pleine largeur** - Plus facile à utiliser
4. ⏳ **Interface d'édition de la section programmes de l'accueil** (non encore activée)

## Pour activer TOUTES les fonctionnalités

Sur le serveur de production, exécute ces commandes dans l'ordre:

```bash
# 1. Aller dans le répertoire du projet
cd /var/www/fitgang

# 2. Sauvegarder l'état actuel (au cas où)
git stash

# 3. Récupérer TOUTES les modifications
git fetch origin
git checkout claude/fix-email-campaigns-011CV29exAWnnTfzcJ4vZoRk
git pull origin claude/fix-email-campaigns-011CV29exAWnnTfzcJ4vZoRk

# 4. Vérifier que tous les fichiers sont présents
echo "Vérification des fichiers clés..."
ls -la app/forms.py | grep -q "HomepageProgrammesForm" && echo "✓ forms.py OK" || echo "✗ forms.py manquant"
ls -la app/templates/admin_homepage_programmes.html && echo "✓ Template OK" || echo "✗ Template manquant"

# 5. Redémarrer l'application
sudo systemctl restart fitgang

# 6. Vérifier les logs
sudo journalctl -u fitgang -n 20 --no-pager
```

## Après le déploiement complet

Tu auras accès à:

### Dans `/admin/homepage-programmes`:
- Modifier le titre de la section programmes
- Modifier le sous-titre
- Modifier les 4 programmes affichés sur la page d'accueil:
  - Badge (ex: POPULAIRE, TOP VENTES)
  - Couleur du badge
  - Titre, description, prix
  - Caractéristiques (une par ligne)
  - URL de l'image

### Dans `/admin` (dashboard):
- Un nouveau bouton "Programmes Accueil" apparaîtra

## Si quelque chose ne fonctionne pas

### Retour en arrière rapide:
```bash
cd /var/www/fitgang
git checkout main  # ou ta branche principale
sudo systemctl restart fitgang
```

### Consulter les logs d'erreur:
```bash
# Logs du service
sudo journalctl -u fitgang -n 50 --no-pager

# Logs Python (si configuré)
tail -f /var/log/fitgang/error.log
```

## Fichiers modifiés dans cette branche

- `app/routes.py` - Ajout route `admin_homepage_programmes` + modification `index()`
- `app/forms.py` - Ajout `HomepageProgrammesForm`
- `app/templates/admin_homepage_programmes.html` - Nouveau template
- `app/templates/admin_dashboard.html` - Dashboard en pleine largeur
- `app/templates/admin_email_campaign_detail.html` - Page en pleine largeur
- `app/templates/base.html` - Support container-fluid
- `app/templates/programmes.html` - Images uniformes 300px
- `app/templates/index.html` - (Temporairement en version statique)

## Important

Pour le moment, la page d'accueil affiche les programmes EN DUR (codés dans le template).
Une fois que tout sera déployé correctement, on pourra réactiver la version dynamique qui permet de modifier les programmes depuis l'interface admin.
