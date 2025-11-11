# 📊 Guide Analytics - Système de tracking des visiteurs

## Vue d'ensemble

FitGang dispose maintenant d'un système d'analytics intégré, comme Google Analytics mais en plus simple et directement dans ton dashboard admin!

## ✨ Fonctionnalités

### Dans le Dashboard Admin

#### 1. **Visiteurs en Direct** 🟢
- Affiche le nombre de visiteurs sur le site **maintenant** (15 dernières minutes)
- Met à jour en temps réel
- Badge vert "EN DIRECT"

#### 2. **Stats Quotidiennes**
- Aujourd'hui: nombre de visiteurs uniques et pages vues
- Hier: pour comparer avec aujourd'hui
- Évolution sur 7 jours (graphique en barres)

#### 3. **Stats Période**
- 7 derniers jours
- 30 derniers jours
- Total all-time

#### 4. **Pages les Plus Visitées**
- Top 5 des pages les plus consultées aujourd'hui
- Nombre de vues par page

#### 5. **Graphique d'Évolution**
- Barre graph montrant les 7 derniers jours
- Voir les tendances et pics d'activité

## 🚀 Déploiement

### Étape 1: Mettre à jour le code

```bash
cd /home/wrbh3411/fitgang.fr
git pull origin claude/fix-email-campaigns-011CV29exAWnnTfzcJ4vZoRk
```

### Étape 2: Créer la table `visits` dans la base de données

**Option A: Avec Flask-Migrate (recommandé)**

```bash
# Activer le virtualenv
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate

# Créer la migration
flask db migrate -m "Add Visit model for analytics"

# Appliquer la migration
flask db upgrade
```

**Option B: Manuellement avec Python**

```bash
# Activer le virtualenv
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate

# Lancer Python
python

# Dans le shell Python:
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

**Option C: SQL Direct (si les options ci-dessus ne fonctionnent pas)**

```sql
CREATE TABLE visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address VARCHAR(50),
    user_agent VARCHAR(500),
    page VARCHAR(500),
    referer VARCHAR(500),
    user_id INTEGER,
    session_id VARCHAR(100),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    country VARCHAR(100),
    city VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE INDEX ix_visits_session_id ON visits (session_id);
CREATE INDEX ix_visits_timestamp ON visits (timestamp);
```

### Étape 3: Redémarrer l'application

```bash
mkdir -p tmp
touch tmp/restart.txt
```

### Étape 4: Vérifier que ça fonctionne

1. Va sur https://fitgang.fr/admin
2. Tu devrais voir une nouvelle section "Analytics & Visiteurs" en haut
3. Navigue sur quelques pages du site
4. Retourne au dashboard admin → Les stats devraient s'incrémenter!

## 📈 Comment ça fonctionne?

### Tracking automatique

- **Chaque visite** sur le site est automatiquement enregistrée
- Enregistre:
  - Page visitée
  - IP du visiteur
  - Navigateur utilisé
  - D'où vient le visiteur (referer)
  - Si connecté: ID utilisateur
  - Session unique pour compter les visiteurs uniques

### Ce qui N'est PAS tracké

- Fichiers statiques (CSS, JS, images)
- Requêtes AJAX
- Bots (partiellement filtré)

### Visiteurs uniques

Un visiteur unique = une session unique (identifié par cookie de session)
Même si quelqu'un visite 10 pages, il compte comme 1 visiteur.

## 🔧 Fonctions disponibles dans le code

### `track_visit()`
Enregistre automatiquement chaque visite (appelé sur chaque requête)

### `get_visitor_stats()`
Retourne toutes les stats sous forme de dictionnaire:
```python
{
    'visitors_live': 5,           # Visiteurs en direct (15 min)
    'pageviews_live': 12,          # Pages vues en direct
    'visitors_today': 45,          # Visiteurs aujourd'hui
    'pageviews_today': 123,        # Pages vues aujourd'hui
    'visitors_yesterday': 38,      # Hier
    'visitors_week': 234,          # 7 jours
    'visitors_month': 789,         # 30 jours
    'visitors_total': 2345,        # Total
    'top_pages_today': [           # Top pages
        ('/programmes', 45),
        ('/', 32),
        ...
    ],
    'visitors_trend': [            # Évolution 7 jours
        {'date': '04/11', 'count': 45},
        {'date': '05/11', 'count': 52},
        ...
    ]
}
```

### `get_hourly_stats_today()`
Stats par heure pour aujourd'hui (voir les pics d'activité)

### `cleanup_old_visits(days=90)`
Nettoie les visites anciennes pour ne pas surcharger la DB
Par défaut: garde 90 jours d'historique

## 🗑️ Maintenance

### Nettoyer automatiquement les vieilles visites

Tu peux créer un cron job pour nettoyer régulièrement:

**Créer le script `cleanup_visits.py`:**
```python
from app import create_app, db
from app.analytics import cleanup_old_visits

app = create_app()
with app.app_context():
    deleted = cleanup_old_visits(days=90)  # Garde 90 jours
    print(f"✓ {deleted} visites anciennes supprimées")
```

**Ajouter au crontab (1x par semaine):**
```bash
# Éditer crontab
crontab -e

# Ajouter cette ligne (exécute le dimanche à 3h du matin):
0 3 * * 0 cd /home/wrbh3411/fitgang.fr && source virtualenv/fitgang.fr/3.6/bin/activate && python cleanup_visits.py
```

## 📊 Exemples d'utilisation

### Voir les stats dans une route personnalisée

```python
from app.analytics import get_visitor_stats

@bp.route('/stats')
@login_required
@admin_required
def custom_stats():
    stats = get_visitor_stats()
    return jsonify(stats)
```

### Tracker des événements spéciaux

```python
from app.models import Visit
from app import db

# Tracker un événement spécial
visit = Visit(
    page="/checkout/success",
    user_id=current_user.id,
    session_id=session.get('visitor_session_id')
)
db.session.add(visit)
db.session.commit()
```

## 🔐 Privacy & RGPD

### Données collectées

- IP (peut être anonymisée)
- User agent (navigateur)
- Pages visitées
- Referer
- User ID si connecté

### Conformité RGPD

Pour être conforme:

1. **Ajouter dans ta politique de confidentialité:**
   "Nous collectons des données de navigation anonymes pour améliorer notre service"

2. **Anonymiser les IPs (optionnel):**

Éditer `app/analytics.py`:
```python
def anonymize_ip(ip):
    """Anonymise une IP en remplaçant le dernier octet par 0"""
    parts = ip.split('.')
    if len(parts) == 4:
        parts[-1] = '0'
        return '.'.join(parts)
    return ip

# Dans track_visit():
ip_address=anonymize_ip(request.remote_addr)
```

3. **Permettre l'opt-out:**

Ajouter un cookie de consentement avant de tracker.

## 🎯 Avantages vs Google Analytics

### ✅ Avantages

- **Propriété des données**: Tout est dans ta DB
- **Pas de cookies tiers**: Meilleur pour le RGPD
- **Pas de script externe**: Performance
- **Personnalisable**: Tu contrôles tout
- **Gratuit**: Pas de limite de vues
- **Privé**: Pas de partage avec Google

### ❌ Limitations

- Pas de données géographiques détaillées
- Pas d'événements avancés (scroll, clics, etc.)
- Pas de segmentation avancée
- Prend de l'espace DB (solution: nettoyage régulier)

## 🚀 Améliorations futures possibles

### 1. Géolocalisation
Ajouter un service comme MaxMind GeoIP pour:
- Pays du visiteur
- Ville
- Afficher sur une carte

### 2. Tracking d'événements
Tracker des actions spécifiques:
- Clics sur boutons "Acheter"
- Inscription newsletter
- Téléchargement ebook
- Vidéos regardées

### 3. Funnels de conversion
Suivre le parcours:
Page d'accueil → Programme → Paiement → Succès

### 4. Temps passé sur page
Calculer combien de temps les utilisateurs restent

### 5. Taux de rebond
% de visiteurs qui quittent après 1 seule page

## 🐛 Troubleshooting

### Les stats ne s'affichent pas

1. **Vérifier que la table existe:**
```bash
sqlite3 fitgang.db
.tables
# Tu devrais voir "visits" dans la liste
```

2. **Vérifier les logs:**
```bash
tail -f ~/logs/error.log
```

3. **Tester manuellement:**
```python
from app import create_app
from app.analytics import get_visitor_stats

app = create_app()
with app.app_context():
    stats = get_visitor_stats()
    print(stats)
```

### Les visites ne sont pas enregistrées

1. **Vérifier que le tracking fonctionne:**
```python
# Dans app/__init__.py, vérifier que before_request est bien défini
# et appelle track_visit()
```

2. **Vérifier les permissions DB:**
```bash
ls -la fitgang.db
# Le fichier doit être writable par l'utilisateur web
```

### La DB grossit trop

Nettoyer régulièrement:
```python
from app.analytics import cleanup_old_visits
cleanup_old_visits(days=30)  # Garde seulement 30 jours
```

## 💡 Conseils d'utilisation

1. **Regarde les stats chaque jour** pour voir l'évolution
2. **Identifie les pages populaires** et optimise-les
3. **Regarde les heures de pic** pour lancer des campagnes au bon moment
4. **Compare avant/après** quand tu fais des changements
5. **Nettoie régulièrement** pour ne pas surcharger la DB

## 📞 Support

Si tu as des questions ou problèmes avec le système analytics, n'hésite pas à demander!
