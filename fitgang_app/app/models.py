"""
Modèles de base de données pour l'application FitGang
Définit les tables User, Programme, Ebook, Achat et Progression
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """
    Modèle utilisateur
    Gère l'authentification et les informations personnelles
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    nom = db.Column(db.String(100))
    poids = db.Column(db.Float)  # en kg
    taille = db.Column(db.Integer)  # en cm
    objectifs = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    achats = db.relationship('Achat', backref='utilisateur', lazy='dynamic', cascade='all, delete-orphan')
    progressions = db.relationship('Progression', backref='utilisateur', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash le mot de passe avant de le stocker"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie si le mot de passe fourni correspond au hash"""
        return check_password_hash(self.password_hash, password)

    def has_purchased(self, item_id, item_type):
        """Vérifie si l'utilisateur a acheté un programme ou ebook spécifique"""
        return Achat.query.filter_by(
            user_id=self.id,
            item_id=item_id,
            type=item_type
        ).first() is not None

    def get_programmes(self):
        """Retourne tous les programmes achetés par l'utilisateur"""
        achats = Achat.query.filter_by(user_id=self.id, type='programme').all()
        return [Programme.query.get(a.item_id) for a in achats]

    def get_ebooks(self):
        """Retourne tous les ebooks achetés par l'utilisateur"""
        achats = Achat.query.filter_by(user_id=self.id, type='ebook').all()
        return [Ebook.query.get(a.item_id) for a in achats]

    def __repr__(self):
        return f'<User {self.email}>'


class Programme(db.Model):
    """
    Modèle programme fitness
    Représente un programme d'entraînement vendable
    """
    __tablename__ = 'programmes'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(300))  # URL ou chemin de l'image
    prix = db.Column(db.Float, nullable=False)  # en euros
    niveau = db.Column(db.String(50))  # Débutant, Intermédiaire, Avancé
    duree = db.Column(db.String(50))  # ex: "8 semaines", "3 mois"
    contenu = db.Column(db.Text)  # Description détaillée du contenu
    actif = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Programme {self.titre}>'


class Ebook(db.Model):
    """
    Modèle ebook
    Représente un livre numérique vendable
    """
    __tablename__ = 'ebooks'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    prix = db.Column(db.Float, nullable=False)  # en euros
    image = db.Column(db.String(300))  # URL ou chemin de l'image de couverture
    lien = db.Column(db.String(500))  # Lien de téléchargement (Google Drive, Dropbox, etc.)
    fichier = db.Column(db.String(300))  # Ou chemin du fichier PDF stocké localement
    nombre_pages = db.Column(db.Integer)
    actif = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Ebook {self.titre}>'


class Achat(db.Model):
    """
    Modèle achat
    Enregistre les achats de programmes et ebooks par les utilisateurs
    """
    __tablename__ = 'achats'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)  # ID du programme ou ebook
    type = db.Column(db.String(20), nullable=False)  # 'programme' ou 'ebook'
    prix_paye = db.Column(db.Float, nullable=False)
    stripe_session_id = db.Column(db.String(200))  # ID de session Stripe
    date_achat = db.Column(db.DateTime, default=datetime.utcnow)

    def get_item(self):
        """Retourne l'objet programme ou ebook acheté"""
        if self.type == 'programme':
            return Programme.query.get(self.item_id)
        elif self.type == 'ebook':
            return Ebook.query.get(self.item_id)
        return None

    def __repr__(self):
        return f'<Achat {self.type} #{self.item_id} by User #{self.user_id}>'


class Progression(db.Model):
    """
    Modèle progression
    Permet aux utilisateurs de suivre leurs séances et progrès
    """
    __tablename__ = 'progressions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    seance = db.Column(db.String(200))  # Nom de la séance (ex: "Jour 1 - Pectoraux")
    poids = db.Column(db.Float)  # Poids du jour
    notes = db.Column(db.Text)  # Notes libres sur la séance
    exercices = db.Column(db.Text)  # Liste des exercices effectués (peut être JSON)

    def __repr__(self):
        return f'<Progression User #{self.user_id} - {self.date}>'
