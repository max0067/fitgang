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
    lien = StringField('Lien de téléchargement', validators=[Optional(), Length(max=500)])
    nombre_pages = IntegerField('Nombre de pages', validators=[Optional(), NumberRange(min=1, max=9999)])
    actif = BooleanField('Ebook actif')
    submit = SubmitField('Enregistrer')
