# 📝 Guide: Rendre le Contenu des Programmes Éditable

## Ce qui sera éditable

Pour chaque programme, tu pourras modifier:

### 1. CE QUI EST INCLUS (6 éléments)
Chaque élément a:
- Icône (choix dans une liste)
- Titre
- Description

### 2. CONTENU DU PROGRAMME
Texte libre avec formatage markdown

### 3. TRANSFORMATIONS RÉELLES (3 témoignages)
Chaque transformation a:
- Photo (URL)
- Nom
- Résultat (ex: "-12kg en 8 semaines")
- Témoignage

### 4. POURQUOI CHOISIR CE PROGRAMME (5 bénéfices)
Chaque bénéfice a:
- Icône (choix dans une liste)
- Titre
- Description

## 🚀 Installation Rapide

### Étape 1: Mettre à jour la base de données

```bash
cd /home/wrbh3411/fitgang.fr
git pull origin claude/fix-email-campaigns-011CV29exAWnnTfzcJ4vZoRk

# Activer virtualenv
source /home/wrbh3411/virtualenv/fitgang.fr/3.6/bin/activate

# Ajouter la colonne content_json
sqlite3 fitgang.db "ALTER TABLE programmes ADD COLUMN content_json TEXT;"
```

### Étape 2: Accéder à l'interface d'édition

1. Va sur https://fitgang.fr/admin/programmes
2. Clique sur un programme
3. Nouveau bouton: **"✏️ Éditer le Contenu de la Page"**
4. Remplis les sections
5. Sauvegarde!

## 📋 Structure du Contenu (Format JSON)

Le contenu est stocké en JSON dans la DB:

```json
{
  "included_items": [
    {
      "icon": "bi-journal-text",
      "title": "Programme Complet",
      "description": "Tous les exercices détaillés..."
    }
  ],
  "program_content": "Texte du contenu du programme...",
  "transformations": [
    {
      "image": "https://...",
      "name": "Maxime L.",
      "result": "-12kg en 8 semaines",
      "testimonial": "Programme complet..."
    }
  ],
  "benefits": [
    {
      "icon": "bi-award",
      "title": "Conçu par des Experts",
      "description": "Élaboré par des coachs..."
    }
  ]
}
```

## 🎨 Icônes Disponibles (Bootstrap Icons)

### Pour "CE QUI EST INCLUS":
- `bi-journal-text` - Programme Complet
- `bi-egg-fried` - Nutrition
- `bi-graph-up-arrow` - Progression
- `bi-play-circle` - Vidéos
- `bi-phone` - Application Mobile
- `bi-people` - Communauté

### Pour "POURQUOI CHOISIR":
- `bi-award` - Expert
- `bi-trophy` - Résultats
- `bi-clock` - Flexible
- `bi-headset` - Support
- `bi-gift` - Gratuit

Voir toutes les icônes: https://icons.getbootstrap.com/

## 💡 Usage dans le Code

### Dans une route:

```python
@bp.route('/programme/<int:programme_id>')
def programme_detail(programme_id):
    programme = Programme.query.get_or_404(programme_id)
    content = programme.get_content_data()

    return render_template('programme_detail.html',
                         programme=programme,
                         content=content)
```

### Dans le template:

```jinja2
{% for item in content.included_items %}
<div class="included-item">
    <i class="{{ item.icon }}"></i>
    <h3>{{ item.title }}</h3>
    <p>{{ item.description }}</p>
</div>
{% endfor %}
```

## 🔧 Fichiers Modifiés

1. **app/models.py**
   - Ajout champ `content_json`
   - Méthode `get_content_data()`

2. **app/routes.py** (à créer)
   - Route `/admin/programme/<id>/edit-content`

3. **app/templates/admin_programme_edit_content.html** (à créer)
   - Formulaire d'édition complet

4. **app/templates/programme_detail.html** (à modifier)
   - Utiliser `content` au lieu du HTML en dur

## 📝 TODO pour finir l'implémentation

- [ ] Créer la route d'édition dans routes.py
- [ ] Créer le template d'édition
- [ ] Mettre à jour programme_detail.html pour utiliser les données
- [ ] Ajouter un lien "Éditer Contenu" dans la liste des programmes admin
- [ ] Tester sur un programme

---

**Status:** Infrastructure en place, reste l'interface d'édition à créer.

Veux-tu que je continue et crée l'interface complète maintenant?
