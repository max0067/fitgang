"""
Point d'entrée de l'application FitGang
Lance le serveur Flask en mode développement
"""
import os
from app import create_app, db
from app.models import User, Programme, Ebook, Achat, Progression

# Créer l'application avec la configuration appropriée
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)


@app.shell_context_processor
def make_shell_context():
    """
    Ajoute automatiquement les modèles au contexte du shell Flask
    Permet d'utiliser 'flask shell' sans importer manuellement les modèles
    """
    return {
        'db': db,
        'User': User,
        'Programme': Programme,
        'Ebook': Ebook,
        'Achat': Achat,
        'Progression': Progression
    }


@app.cli.command()
def init_db():
    """Initialise la base de données"""
    db.create_all()
    print("✅ Base de données initialisée avec succès!")


@app.cli.command()
def create_admin():
    """Crée un utilisateur administrateur"""
    from werkzeug.security import generate_password_hash

    email = input("Email de l'admin: ")
    password = input("Mot de passe: ")
    prenom = input("Prénom: ")

    # Vérifier si l'utilisateur existe déjà
    if User.query.filter_by(email=email).first():
        print("❌ Un utilisateur avec cet email existe déjà!")
        return

    # Créer l'admin
    admin = User(
        email=email,
        password_hash=generate_password_hash(password),
        prenom=prenom,
        is_admin=True
    )

    db.session.add(admin)
    db.session.commit()
    print(f"✅ Admin {prenom} créé avec succès!")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
