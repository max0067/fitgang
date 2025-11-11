"""
Formulaires Flask-WTF pour l'application FitGang
Gère la validation des données côté serveur
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional, Length, NumberRange
from app.models import User


class LoginForm(FlaskForm):
    """Formulaire de connexion"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')


class RegistrationForm(FlaskForm):
    """Formulaire d'inscription"""
    prenom = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=100)])
    nom = StringField('Nom', validators=[Optional(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        Length(min=6, message='Le mot de passe doit contenir au moins 6 caractères')
    ])
    password2 = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', message='Les mots de passe doivent correspondre')
    ])
    submit = SubmitField("S'inscrire")

    def validate_email(self, email):
        """Vérifie que l'email n'est pas déjà utilisé"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé. Veuillez en choisir un autre.')


class ProfileForm(FlaskForm):
    """Formulaire de modification du profil utilisateur"""
    prenom = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=100)])
    nom = StringField('Nom', validators=[Optional(), Length(max=100)])
    poids = FloatField('Poids (kg)', validators=[Optional(), NumberRange(min=30, max=300)])
    taille = IntegerField('Taille (cm)', validators=[Optional(), NumberRange(min=100, max=250)])
    objectifs = TextAreaField('Objectifs fitness', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Mettre à jour')


class ChangePasswordForm(FlaskForm):
    """Formulaire de changement de mot de passe"""
    old_password = PasswordField('Mot de passe actuel', validators=[DataRequired()])
    new_password = PasswordField('Nouveau mot de passe', validators=[
        DataRequired(),
        Length(min=6, message='Le mot de passe doit contenir au moins 6 caractères')
    ])
    new_password2 = PasswordField('Confirmer le nouveau mot de passe', validators=[
        DataRequired(),
        EqualTo('new_password', message='Les mots de passe doivent correspondre')
    ])
    submit = SubmitField('Changer le mot de passe')


class ProgressionForm(FlaskForm):
    """Formulaire d'ajout de progression"""
    seance = StringField('Nom de la séance', validators=[DataRequired(), Length(max=200)])
    poids = FloatField('Poids du jour (kg)', validators=[Optional(), NumberRange(min=30, max=300)])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=2000)])
    exercices = TextAreaField('Exercices effectués', validators=[Optional(), Length(max=2000)])
    submit = SubmitField('Enregistrer la séance')


# ===== FORMULAIRES ADMIN =====

class ProgrammeForm(FlaskForm):
    """Formulaire de création/modification de programme"""
    titre = StringField('Titre', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description courte', validators=[DataRequired(), Length(max=500)])
    contenu = TextAreaField('Contenu détaillé', validators=[Optional()])
    prix = FloatField('Prix (€)', validators=[DataRequired(), NumberRange(min=0, max=9999)])
    niveau = SelectField('Niveau', choices=[
        ('Débutant', 'Débutant'),
        ('Intermédiaire', 'Intermédiaire'),
        ('Avancé', 'Avancé')
    ], validators=[DataRequired()])
    duree = StringField('Durée', validators=[DataRequired(), Length(max=50)])
    image = StringField('URL de l\'image', validators=[Optional(), Length(max=300)])
    actif = BooleanField('Programme actif')
    submit = SubmitField('Enregistrer')


class EbookForm(FlaskForm):
    """Formulaire de création/modification d'ebook"""
    titre = StringField('Titre', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1000)])
    prix = FloatField('Prix (€)', validators=[DataRequired(), NumberRange(min=0, max=9999)])
    image = StringField('URL de l\'image de couverture', validators=[Optional(), Length(max=300)])
    fichier = FileField('Fichier PDF/EPUB', validators=[Optional(), FileAllowed(['pdf', 'epub'], 'Seulement les fichiers PDF et EPUB!')])
    lien = StringField('Lien de téléchargement externe (optionnel)', validators=[Optional(), Length(max=500)])
    nombre_pages = IntegerField('Nombre de pages', validators=[Optional(), NumberRange(min=1, max=9999)])
    actif = BooleanField('Ebook actif')
    submit = SubmitField('Enregistrer')


class SeanceForm(FlaskForm):
    """Formulaire de création/modification de séance de programme"""
    semaine = IntegerField('Semaine', validators=[DataRequired(), NumberRange(min=1, max=52)])
    jour = IntegerField('Jour', validators=[DataRequired(), NumberRange(min=1, max=7)])
    titre = StringField('Titre de la séance', validators=[DataRequired(), Length(max=200)])
    exercices = TextAreaField('Exercices détaillés', validators=[DataRequired(), Length(max=5000)])
    notes = TextAreaField('Instructions/Notes', validators=[Optional(), Length(max=2000)])
    submit = SubmitField('Enregistrer')


class ComplementForm(FlaskForm):
    """Formulaire de création/modification de complément alimentaire"""
    nom = StringField('Nom du produit', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=2000)])
    prix = FloatField('Prix (€)', validators=[DataRequired(), NumberRange(min=0, max=9999)])
    categorie = SelectField('Catégorie', choices=[
        ('Protéines', 'Protéines'),
        ('Créatine', 'Créatine'),
        ('Pre-workout', 'Pre-workout'),
        ('Vitamines', 'Vitamines'),
        ('Oméga-3', 'Oméga-3'),
        ('BCAA', 'BCAA'),
        ('Gainers', 'Gainers'),
        ('Brûleurs de graisse', 'Brûleurs de graisse'),
        ('Autre', 'Autre')
    ], validators=[DataRequired()])
    marque = StringField('Marque', validators=[Optional(), Length(max=100)])
    dosage = StringField('Dosage recommandé', validators=[Optional(), Length(max=200)])
    image = StringField('URL de l\'image', validators=[Optional(), Length(max=300)])
    lien_achat = StringField('Lien d\'achat', validators=[Optional(), Length(max=500)])
    actif = BooleanField('Complément actif')
    submit = SubmitField('Enregistrer')


class HomepageContentForm(FlaskForm):
    """Formulaire d'édition du contenu de la page d'accueil"""
    hero_titre = StringField('Titre principal (Hero)', validators=[DataRequired(), Length(max=200)])
    hero_sous_titre = TextAreaField('Sous-titre (Hero)', validators=[DataRequired(), Length(max=500)])

    stat_membres = StringField('Statistique - Membres', validators=[DataRequired(), Length(max=50)])
    stat_programmes = StringField('Statistique - Programmes', validators=[DataRequired(), Length(max=50)])
    stat_transformations = StringField('Statistique - Transformations', validators=[DataRequired(), Length(max=50)])
    stat_satisfaction = StringField('Statistique - Satisfaction', validators=[DataRequired(), Length(max=50)])

    philosophie_titre = StringField('Titre section philosophie', validators=[DataRequired(), Length(max=200)])
    philosophie_texte = TextAreaField('Texte section philosophie', validators=[DataRequired(), Length(max=1000)])

    cta_titre = StringField('Titre appel à l\'action final', validators=[DataRequired(), Length(max=200)])
    cta_texte = TextAreaField('Texte appel à l\'action final', validators=[DataRequired(), Length(max=500)])

    submit = SubmitField('Enregistrer les modifications')


class EmailCampaignForm(FlaskForm):
    """Formulaire de création de campagne d'email"""
    nom = StringField('Nom de la campagne', validators=[DataRequired(), Length(max=200)])
    sujet = StringField('Sujet de l\'email', validators=[DataRequired(), Length(max=300)])
    contenu_html = TextAreaField('Contenu HTML', validators=[DataRequired()], render_kw={"rows": 15})
    contenu_texte = TextAreaField('Contenu texte (optionnel)', validators=[Optional()], render_kw={"rows": 10})
    submit = SubmitField('Créer la campagne')


class EmailImportForm(FlaskForm):
    """Formulaire d'import de liste d'emails"""
    fichier_csv = FileField('Fichier CSV d\'emails', validators=[DataRequired(), FileAllowed(['csv', 'txt'], 'Seulement les fichiers CSV et TXT!')])
    submit = SubmitField('Importer les emails')


class HomepageProgrammesForm(FlaskForm):
    """Formulaire pour éditer la section programmes de la page d'accueil"""
    # Titre de la section
    section_titre = StringField('Titre de la section', validators=[DataRequired(), Length(max=200)])
    section_sous_titre = TextAreaField('Sous-titre de la section', validators=[DataRequired(), Length(max=500)])
    
    # Programme 1
    prog1_badge = StringField('Badge (optionnel)', validators=[Optional(), Length(max=50)])
    prog1_badge_color = SelectField('Couleur du badge', choices=[('', 'Aucun'), ('bg-warning', 'Jaune (Warning)'), ('bg-danger', 'Rouge (Danger)'), ('bg-success', 'Vert (Success)'), ('bg-info', 'Bleu (Info)')], validators=[Optional()])
    prog1_titre = StringField('Titre', validators=[DataRequired(), Length(max=100)])
    prog1_description = TextAreaField('Description', validators=[DataRequired(), Length(max=300)])
    prog1_features = TextAreaField('Caractéristiques (une par ligne)', validators=[DataRequired()])
    prog1_prix = StringField('Prix', validators=[DataRequired(), Length(max=20)])
    prog1_image = StringField('URL de l\'image', validators=[DataRequired(), Length(max=500)])
    
    # Programme 2
    prog2_badge = StringField('Badge (optionnel)', validators=[Optional(), Length(max=50)])
    prog2_badge_color = SelectField('Couleur du badge', choices=[('', 'Aucun'), ('bg-warning', 'Jaune (Warning)'), ('bg-danger', 'Rouge (Danger)'), ('bg-success', 'Vert (Success)'), ('bg-info', 'Bleu (Info)')], validators=[Optional()])
    prog2_titre = StringField('Titre', validators=[DataRequired(), Length(max=100)])
    prog2_description = TextAreaField('Description', validators=[DataRequired(), Length(max=300)])
    prog2_features = TextAreaField('Caractéristiques (une par ligne)', validators=[DataRequired()])
    prog2_prix = StringField('Prix', validators=[DataRequired(), Length(max=20)])
    prog2_image = StringField('URL de l\'image', validators=[DataRequired(), Length(max=500)])
    
    # Programme 3
    prog3_badge = StringField('Badge (optionnel)', validators=[Optional(), Length(max=50)])
    prog3_badge_color = SelectField('Couleur du badge', choices=[('', 'Aucun'), ('bg-warning', 'Jaune (Warning)'), ('bg-danger', 'Rouge (Danger)'), ('bg-success', 'Vert (Success)'), ('bg-info', 'Bleu (Info)')], validators=[Optional()])
    prog3_titre = StringField('Titre', validators=[DataRequired(), Length(max=100)])
    prog3_description = TextAreaField('Description', validators=[DataRequired(), Length(max=300)])
    prog3_features = TextAreaField('Caractéristiques (une par ligne)', validators=[DataRequired()])
    prog3_prix = StringField('Prix', validators=[DataRequired(), Length(max=20)])
    prog3_image = StringField('URL de l\'image', validators=[DataRequired(), Length(max=500)])
    
    # Programme 4
    prog4_badge = StringField('Badge (optionnel)', validators=[Optional(), Length(max=50)])
    prog4_badge_color = SelectField('Couleur du badge', choices=[('', 'Aucun'), ('bg-warning', 'Jaune (Warning)'), ('bg-danger', 'Rouge (Danger)'), ('bg-success', 'Vert (Success)'), ('bg-info', 'Bleu (Info)')], validators=[Optional()])
    prog4_titre = StringField('Titre', validators=[DataRequired(), Length(max=100)])
    prog4_description = TextAreaField('Description', validators=[DataRequired(), Length(max=300)])
    prog4_features = TextAreaField('Caractéristiques (une par ligne)', validators=[DataRequired()])
    prog4_prix = StringField('Prix', validators=[DataRequired(), Length(max=20)])
    prog4_image = StringField('URL de l\'image', validators=[DataRequired(), Length(max=500)])
    
    submit = SubmitField('Sauvegarder les modifications')
