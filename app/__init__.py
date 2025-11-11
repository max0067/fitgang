"""
Initialisation de l'application Flask FitGang
Configure les extensions et les blueprints
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

# Initialisation des extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Flask-Mail optionnel
try:
    from flask_mail import Mail
    mail = Mail()
    MAIL_ENABLED = True
except ImportError:
    mail = None
    MAIL_ENABLED = False


def create_app(config_name='default'):
    """
    Factory pattern pour créer l'application Flask
    Permet de créer plusieurs instances avec des configurations différentes
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Force template reloading in development
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # Configuration pour l'upload de fichiers
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB max
    app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'epub'}

    # Créer le dossier uploads s'il n'existe pas
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialiser les extensions avec l'app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Initialiser Flask-Mail si disponible
    if MAIL_ENABLED and mail:
        mail.init_app(app)

    # Configuration de Flask-Login
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'warning'

    # Importer et enregistrer les routes
    from app import routes
    app.register_blueprint(routes.bp)

    # Tracking automatique des visites - TEMPORAIREMENT DÉSACTIVÉ
    # @app.before_request
    # def before_request():
    #     """Track chaque visite pour les analytics"""
    #     try:
    #         from app.analytics import track_visit
    #         track_visit()
    #     except Exception as e:
    #         # Ne pas bloquer l'app si le tracking échoue
    #         pass

    # Ne pas utiliser db.create_all() en production avec des migrations
    # Les tables sont gérées par Flask-Migrate (flask db upgrade)
    # with app.app_context():
    #     db.create_all()

    return app


@login_manager.user_loader
def load_user(user_id):
    """
    Callback requis par Flask-Login pour charger un utilisateur
    à partir de son ID stocké en session
    """
    from app.models import User
    return User.query.get(int(user_id))
