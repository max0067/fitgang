"""
Routes de l'application FitGang
Gère toutes les vues utilisateur et administrateur
"""
import os
import stripe
import secrets
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, session, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from app import db
from app.models import User, Programme, Ebook, Achat, Progression
from app.forms import (LoginForm, RegistrationForm, ProfileForm, ChangePasswordForm,
                       ProgressionForm, ProgrammeForm, EbookForm)

# Créer le blueprint
bp = Blueprint('main', __name__)

# Configuration Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_your_key_here')


# ===== DÉCORATEURS =====

def admin_required(f):
    """Décorateur pour restreindre l'accès aux administrateurs"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Vous devez être administrateur pour accéder à cette page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


def save_ebook_file(file):
    """
    Sauvegarde un fichier ebook uploadé de manière sécurisée
    Retourne le nom du fichier sauvegardé
    """
    if file:
        # Générer un nom de fichier unique et sécurisé
        random_hex = secrets.token_hex(8)
        _, file_ext = os.path.splitext(secure_filename(file.filename))
        filename = f"ebook_{random_hex}{file_ext}"

        # Sauvegarder le fichier
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        return filename
    return None


# ===== ROUTES PUBLIQUES =====

@bp.route('/')
def index():
    """Page d'accueil"""
    programmes = Programme.query.filter_by(actif=True).limit(3).all()
    ebooks = Ebook.query.filter_by(actif=True).limit(3).all()
    return render_template('index.html', programmes=programmes, ebooks=ebooks)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Bienvenue {user.prenom}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Email ou mot de passe incorrect.', 'danger')

    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Page d'inscription"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            prenom=form.prenom.data,
            nom=form.nom.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Votre compte a été créé avec succès! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    """Déconnexion"""
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.index'))


@bp.route('/programmes')
def programmes():
    """Page listant tous les programmes"""
    all_programmes = Programme.query.filter_by(actif=True).all()
    return render_template('programmes.html', programmes=all_programmes)


@bp.route('/programme/<int:id>')
def programme_detail(id):
    """Page de détail d'un programme spécifique"""
    programme = Programme.query.get_or_404(id)

    # Check if user has purchased this program
    has_purchased = False
    if current_user.is_authenticated:
        has_purchased = current_user.has_purchased(id, 'programme')

    return render_template('programme_detail.html', programme=programme, has_purchased=has_purchased)


@bp.route('/programme/<int:id>/access')
@login_required
def programme_access(id):
    """Page d'accès au contenu complet d'un programme acheté"""
    programme = Programme.query.get_or_404(id)

    # Vérifier que l'utilisateur a acheté ce programme
    if not current_user.has_purchased(id, 'programme'):
        flash('Vous devez acheter ce programme pour y accéder.', 'warning')
        return redirect(url_for('main.programme_detail', id=id))

    # Récupérer l'achat pour obtenir la date
    achat = Achat.query.filter_by(
        user_id=current_user.id,
        item_id=id,
        type='programme'
    ).first()

    return render_template('programme_access.html', programme=programme, achat=achat)


@bp.route('/ebooks')
def ebooks():
    """Page listant tous les ebooks"""
    all_ebooks = Ebook.query.filter_by(actif=True).all()
    return render_template('ebooks.html', ebooks=all_ebooks)


@bp.route('/ebook/<int:id>/download')
@login_required
def download_ebook(id):
    """
    Télécharger un ebook acheté
    Vérifie que l'utilisateur a bien acheté l'ebook avant de permettre le téléchargement
    """
    ebook = Ebook.query.get_or_404(id)

    # Vérifier que l'utilisateur a acheté cet ebook
    if not current_user.has_purchased(id, 'ebook'):
        flash('Vous devez acheter cet ebook avant de le télécharger.', 'warning')
        return redirect(url_for('main.ebooks'))

    # Vérifier que le fichier existe
    if not ebook.fichier:
        flash('Ce fichier n\'est pas disponible au téléchargement.', 'danger')
        return redirect(url_for('main.dashboard'))

    # Envoyer le fichier
    try:
        return send_from_directory(
            current_app.config['UPLOAD_FOLDER'],
            ebook.fichier,
            as_attachment=True,
            download_name=f"{ebook.titre}.pdf"
        )
    except FileNotFoundError:
        flash('Le fichier n\'a pas été trouvé.', 'danger')
        return redirect(url_for('main.dashboard'))


# ===== ROUTES UTILISATEUR =====

@bp.route('/dashboard')
@login_required
def dashboard():
    """Tableau de bord utilisateur"""
    mes_programmes = current_user.get_programmes()
    mes_ebooks = current_user.get_ebooks()
    progressions_recentes = Progression.query.filter_by(user_id=current_user.id)\
        .order_by(Progression.date.desc()).limit(5).all()

    return render_template('dashboard.html',
                         programmes=mes_programmes,
                         ebooks=mes_ebooks,
                         progressions=progressions_recentes)


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Page de profil utilisateur"""
    form = ProfileForm()

    if form.validate_on_submit():
        current_user.prenom = form.prenom.data
        current_user.nom = form.nom.data
        current_user.poids = form.poids.data
        current_user.taille = form.taille.data
        current_user.objectifs = form.objectifs.data

        db.session.commit()
        flash('Votre profil a été mis à jour!', 'success')
        return redirect(url_for('main.profile'))

    elif request.method == 'GET':
        form.prenom.data = current_user.prenom
        form.nom.data = current_user.nom
        form.poids.data = current_user.poids
        form.taille.data = current_user.taille
        form.objectifs.data = current_user.objectifs

    return render_template('profile.html', form=form)


@bp.route('/progression/add', methods=['GET', 'POST'])
@login_required
def add_progression():
    """Ajouter une séance de progression"""
    form = ProgressionForm()

    if form.validate_on_submit():
        progression = Progression(
            user_id=current_user.id,
            seance=form.seance.data,
            poids=form.poids.data,
            notes=form.notes.data,
            exercices=form.exercices.data
        )

        db.session.add(progression)
        db.session.commit()

        flash('Séance enregistrée avec succès!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_progression.html', form=form)


@bp.route('/progression/<int:id>/delete', methods=['POST'])
@login_required
def delete_progression(id):
    """Supprimer une progression"""
    progression = Progression.query.get_or_404(id)

    if progression.user_id != current_user.id:
        flash('Vous ne pouvez pas supprimer cette séance.', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.delete(progression)
    db.session.commit()
    flash('Séance supprimée.', 'info')

    return redirect(url_for('main.dashboard'))


# ===== ROUTES STRIPE / PAIEMENT =====

@bp.route('/checkout/<item_type>/<int:item_id>')
@login_required
def checkout(item_type, item_id):
    """Créer une session Stripe Checkout"""
    # Vérifier que l'utilisateur n'a pas déjà acheté cet item
    if current_user.has_purchased(item_id, item_type):
        flash('Vous avez déjà acheté cet article!', 'info')
        return redirect(url_for('main.dashboard'))

    # Récupérer l'item
    if item_type == 'programme':
        item = Programme.query.get_or_404(item_id)
    elif item_type == 'ebook':
        item = Ebook.query.get_or_404(item_id)
    else:
        flash('Type d\'article invalide.', 'danger')
        return redirect(url_for('main.index'))

    try:
        # Créer une session Stripe Checkout
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': item.titre,
                        'description': item.description[:100],
                    },
                    'unit_amount': int(item.prix * 100),  # Stripe utilise les centimes
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('main.checkout_success', _external=True) +
                        f'?session_id={{CHECKOUT_SESSION_ID}}&item_type={item_type}&item_id={item_id}',
            cancel_url=url_for('main.checkout_cancel', _external=True),
            client_reference_id=str(current_user.id),
        )

        return redirect(checkout_session.url, code=303)

    except Exception as e:
        flash(f'Erreur lors de la création de la session de paiement: {str(e)}', 'danger')
        return redirect(url_for('main.index'))


@bp.route('/checkout/success')
@login_required
def checkout_success():
    """Page de succès après paiement"""
    session_id = request.args.get('session_id')
    item_type = request.args.get('item_type')
    item_id = request.args.get('item_id')

    if not all([session_id, item_type, item_id]):
        flash('Informations de paiement manquantes.', 'warning')
        return redirect(url_for('main.dashboard'))

    # Vérifier si l'achat n'a pas déjà été enregistré
    existing_achat = Achat.query.filter_by(
        stripe_session_id=session_id
    ).first()

    if not existing_achat:
        # Récupérer l'item pour le prix
        if item_type == 'programme':
            item = Programme.query.get(item_id)
        else:
            item = Ebook.query.get(item_id)

        # Enregistrer l'achat
        achat = Achat(
            user_id=current_user.id,
            item_id=item_id,
            type=item_type,
            prix_paye=item.prix,
            stripe_session_id=session_id
        )

        db.session.add(achat)
        db.session.commit()

        flash('Paiement réussi! L\'article a été ajouté à votre bibliothèque.', 'success')
    else:
        flash('Cet achat a déjà été enregistré.', 'info')

    return redirect(url_for('main.dashboard'))


@bp.route('/checkout/cancel')
@login_required
def checkout_cancel():
    """Page d'annulation de paiement"""
    flash('Le paiement a été annulé.', 'warning')
    return redirect(url_for('main.index'))


# ===== ROUTES ADMIN =====

@bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Dashboard administrateur"""
    from datetime import timedelta
    from sqlalchemy import func

    # Statistiques générales
    nb_users = User.query.count()
    nb_programmes = Programme.query.count()
    nb_ebooks = Ebook.query.count()
    nb_achats = Achat.query.count()

    # Revenus totaux
    revenus_total = db.session.query(db.func.sum(Achat.prix_paye)).scalar() or 0

    # Date actuelle
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    week_start = now - timedelta(days=7)
    month_start = datetime(now.year, now.month, 1)

    # Revenus par période
    revenus_today = db.session.query(db.func.sum(Achat.prix_paye))\
        .filter(Achat.date_achat >= today_start).scalar() or 0
    revenus_week = db.session.query(db.func.sum(Achat.prix_paye))\
        .filter(Achat.date_achat >= week_start).scalar() or 0
    revenus_month = db.session.query(db.func.sum(Achat.prix_paye))\
        .filter(Achat.date_achat >= month_start).scalar() or 0

    # Nouveaux utilisateurs par période
    new_users_today = User.query.filter(User.date_inscription >= today_start).count()
    new_users_week = User.query.filter(User.date_inscription >= week_start).count()
    new_users_month = User.query.filter(User.date_inscription >= month_start).count()

    # Achats par période
    achats_today = Achat.query.filter(Achat.date_achat >= today_start).count()
    achats_week = Achat.query.filter(Achat.date_achat >= week_start).count()
    achats_month = Achat.query.filter(Achat.date_achat >= month_start).count()

    # Programmes les plus vendus
    top_programmes = db.session.query(
        Programme.titre,
        Programme.prix,
        func.count(Achat.id).label('ventes')
    ).join(Achat, (Achat.item_id == Programme.id) & (Achat.type == 'programme'))\
     .group_by(Programme.id)\
     .order_by(func.count(Achat.id).desc())\
     .limit(5).all()

    # Ebooks les plus vendus
    top_ebooks = db.session.query(
        Ebook.titre,
        Ebook.prix,
        func.count(Achat.id).label('ventes')
    ).join(Achat, (Achat.item_id == Ebook.id) & (Achat.type == 'ebook'))\
     .group_by(Ebook.id)\
     .order_by(func.count(Achat.id).desc())\
     .limit(5).all()

    # Taux de conversion (utilisateurs qui ont acheté au moins 1 fois)
    users_with_purchase = db.session.query(Achat.user_id).distinct().count()
    conversion_rate = (users_with_purchase / nb_users * 100) if nb_users > 0 else 0

    # Valeur moyenne par client
    average_order_value = (revenus_total / nb_achats) if nb_achats > 0 else 0

    # Achats récents
    achats_recents = Achat.query.order_by(Achat.date_achat.desc()).limit(10).all()

    return render_template('admin_dashboard.html',
                         nb_users=nb_users,
                         nb_programmes=nb_programmes,
                         nb_ebooks=nb_ebooks,
                         nb_achats=nb_achats,
                         revenus_total=revenus_total,
                         revenus_today=revenus_today,
                         revenus_week=revenus_week,
                         revenus_month=revenus_month,
                         new_users_today=new_users_today,
                         new_users_week=new_users_week,
                         new_users_month=new_users_month,
                         achats_today=achats_today,
                         achats_week=achats_week,
                         achats_month=achats_month,
                         top_programmes=top_programmes,
                         top_ebooks=top_ebooks,
                         conversion_rate=conversion_rate,
                         average_order_value=average_order_value,
                         achats_recents=achats_recents)


@bp.route('/admin/programmes')
@login_required
@admin_required
def admin_programmes():
    """Liste des programmes (admin)"""
    all_programmes = Programme.query.order_by(Programme.date_creation.desc()).all()
    return render_template('admin_programmes.html', programmes=all_programmes)


@bp.route('/admin/programme/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_programme():
    """Ajouter un programme"""
    form = ProgrammeForm()

    if form.validate_on_submit():
        programme = Programme(
            titre=form.titre.data,
            description=form.description.data,
            contenu=form.contenu.data,
            prix=form.prix.data,
            niveau=form.niveau.data,
            duree=form.duree.data,
            image=form.image.data,
            actif=form.actif.data
        )

        db.session.add(programme)
        db.session.commit()

        flash('Programme créé avec succès!', 'success')
        return redirect(url_for('main.admin_programmes'))

    form.actif.data = True  # Par défaut actif
    return render_template('admin_programme_form.html', form=form, title='Ajouter un programme')


@bp.route('/admin/programme/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_programme(id):
    """Modifier un programme"""
    programme = Programme.query.get_or_404(id)
    form = ProgrammeForm()

    if form.validate_on_submit():
        programme.titre = form.titre.data
        programme.description = form.description.data
        programme.contenu = form.contenu.data
        programme.prix = form.prix.data
        programme.niveau = form.niveau.data
        programme.duree = form.duree.data
        programme.image = form.image.data
        programme.actif = form.actif.data

        db.session.commit()

        flash('Programme mis à jour!', 'success')
        return redirect(url_for('main.admin_programmes'))

    elif request.method == 'GET':
        form.titre.data = programme.titre
        form.description.data = programme.description
        form.contenu.data = programme.contenu
        form.prix.data = programme.prix
        form.niveau.data = programme.niveau
        form.duree.data = programme.duree
        form.image.data = programme.image
        form.actif.data = programme.actif

    return render_template('admin_programme_form.html', form=form, title='Modifier le programme')


@bp.route('/admin/programme/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_programme(id):
    """Supprimer un programme"""
    programme = Programme.query.get_or_404(id)

    db.session.delete(programme)
    db.session.commit()

    flash('Programme supprimé.', 'info')
    return redirect(url_for('main.admin_programmes'))


@bp.route('/admin/ebooks')
@login_required
@admin_required
def admin_ebooks():
    """Liste des ebooks (admin)"""
    all_ebooks = Ebook.query.order_by(Ebook.date_creation.desc()).all()
    return render_template('admin_ebooks.html', ebooks=all_ebooks)


@bp.route('/admin/ebook/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_ebook():
    """Ajouter un ebook"""
    form = EbookForm()

    if form.validate_on_submit():
        # Gérer l'upload du fichier ebook
        fichier_name = None
        if form.fichier.data:
            fichier_name = save_ebook_file(form.fichier.data)

        ebook = Ebook(
            titre=form.titre.data,
            description=form.description.data,
            prix=form.prix.data,
            image=form.image.data,
            fichier=fichier_name,
            lien=form.lien.data,
            nombre_pages=form.nombre_pages.data,
            actif=form.actif.data
        )

        db.session.add(ebook)
        db.session.commit()

        flash('Ebook créé avec succès!', 'success')
        return redirect(url_for('main.admin_ebooks'))

    form.actif.data = True
    return render_template('admin_ebook_form.html', form=form, title='Ajouter un ebook')


@bp.route('/admin/ebook/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_ebook(id):
    """Modifier un ebook"""
    ebook = Ebook.query.get_or_404(id)
    form = EbookForm()

    if form.validate_on_submit():
        # Gérer l'upload d'un nouveau fichier
        if form.fichier.data:
            # Supprimer l'ancien fichier si il existe
            if ebook.fichier:
                old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], ebook.fichier)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Sauvegarder le nouveau fichier
            ebook.fichier = save_ebook_file(form.fichier.data)

        ebook.titre = form.titre.data
        ebook.description = form.description.data
        ebook.prix = form.prix.data
        ebook.image = form.image.data
        ebook.lien = form.lien.data
        ebook.nombre_pages = form.nombre_pages.data
        ebook.actif = form.actif.data

        db.session.commit()

        flash('Ebook mis à jour!', 'success')
        return redirect(url_for('main.admin_ebooks'))

    elif request.method == 'GET':
        form.titre.data = ebook.titre
        form.description.data = ebook.description
        form.prix.data = ebook.prix
        form.image.data = ebook.image
        form.lien.data = ebook.lien
        form.nombre_pages.data = ebook.nombre_pages
        form.actif.data = ebook.actif

    return render_template('admin_ebook_form.html', form=form, title='Modifier l\'ebook', ebook=ebook)


@bp.route('/admin/ebook/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_ebook(id):
    """Supprimer un ebook"""
    ebook = Ebook.query.get_or_404(id)

    db.session.delete(ebook)
    db.session.commit()

    flash('Ebook supprimé.', 'info')
    return redirect(url_for('main.admin_ebooks'))


@bp.route('/admin/users')
@login_required
@admin_required
def admin_users():
    """Liste des utilisateurs (admin)"""
    all_users = User.query.order_by(User.date_inscription.desc()).all()

    # Calculer des stats pour chaque utilisateur
    users_data = []
    for user in all_users:
        nb_achats = Achat.query.filter_by(user_id=user.id).count()
        total_depense = db.session.query(db.func.sum(Achat.prix_paye))\
            .filter_by(user_id=user.id).scalar() or 0

        users_data.append({
            'user': user,
            'nb_achats': nb_achats,
            'total_depense': total_depense
        })

    return render_template('admin_users.html', users_data=users_data)


@bp.route('/admin/user/<int:id>')
@login_required
@admin_required
def admin_user_detail(id):
    """Détail d'un utilisateur (admin)"""
    user = User.query.get_or_404(id)

    # Récupérer tous les achats de l'utilisateur
    achats = Achat.query.filter_by(user_id=user.id)\
        .order_by(Achat.date_achat.desc()).all()

    # Récupérer les progressions
    progressions = Progression.query.filter_by(user_id=user.id)\
        .order_by(Progression.date.desc()).limit(10).all()

    # Stats
    total_depense = db.session.query(db.func.sum(Achat.prix_paye))\
        .filter_by(user_id=user.id).scalar() or 0
    nb_progressions = Progression.query.filter_by(user_id=user.id).count()

    return render_template('admin_user_detail.html',
                         user=user,
                         achats=achats,
                         progressions=progressions,
                         total_depense=total_depense,
                         nb_progressions=nb_progressions)


@bp.route('/admin/user/<int:id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def admin_toggle_admin(id):
    """Basculer le statut admin d'un utilisateur"""
    user = User.query.get_or_404(id)

    # Empêcher de se retirer soi-même les droits admin
    if user.id == current_user.id:
        flash('Vous ne pouvez pas modifier vos propres droits administrateur.', 'warning')
        return redirect(url_for('main.admin_user_detail', id=id))

    user.is_admin = not user.is_admin
    db.session.commit()

    status = "administrateur" if user.is_admin else "utilisateur normal"
    flash(f'{user.prenom} {user.nom} est maintenant {status}.', 'success')

    return redirect(url_for('main.admin_user_detail', id=id))


@bp.route('/admin/user/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(id):
    """Supprimer un utilisateur"""
    user = User.query.get_or_404(id)

    # Empêcher de se supprimer soi-même
    if user.id == current_user.id:
        flash('Vous ne pouvez pas supprimer votre propre compte.', 'danger')
        return redirect(url_for('main.admin_users'))

    # Supprimer d'abord les achats et progressions associés
    Achat.query.filter_by(user_id=user.id).delete()
    Progression.query.filter_by(user_id=user.id).delete()

    db.session.delete(user)
    db.session.commit()

    flash(f'L\'utilisateur {user.prenom} {user.nom} a été supprimé.', 'info')
    return redirect(url_for('main.admin_users'))
