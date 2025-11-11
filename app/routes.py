"""
Routes de l'application FitGang
Gère toutes les vues utilisateur et administrateur
"""
import os
import stripe
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, session, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from app import db
from app.models import User, Programme, Ebook, Achat, Progression, Photo, ProgrammeSeance, ProgrammeProgression, Complement, Newsletter, PageContent, EmailCampaign
from app.forms import (LoginForm, RegistrationForm, ProfileForm, ChangePasswordForm,
                       ProgressionForm, ProgrammeForm, EbookForm, SeanceForm, ComplementForm, HomepageContentForm, HomepageProgrammesForm, EmailCampaignForm, EmailImportForm)
from app.email import send_welcome_email, send_purchase_confirmation_email, send_admin_notification_email
from app.email_bulk import send_test_email, send_bulk_emails, preview_campaign_recipients, get_campaign_stats

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

    # Charger le contenu personnalisable de la page
    def get_content(section, default=''):
        try:
            content = PageContent.query.filter_by(section=section).first()
            return content.contenu if content else default
        except Exception as e:
            print(f"Erreur lors du chargement de PageContent: {e}")
            return default

    page_content = {
        'hero_titre': get_content('hero_titre', 'TRANSFORME TON CORPS, DÉPASSE TES LIMITES'),
        'hero_sous_titre': get_content('hero_sous_titre', 'Rejoins FitGang et découvre des programmes exclusifs pour atteindre tes objectifs fitness. Nutrition, entraînement, mindset : tout pour réussir ta transformation.'),
        'stat_membres': get_content('stat_membres', '10K+ Membres Actifs'),
        'stat_programmes': get_content('stat_programmes', '50+ Programmes'),
        'stat_transformations': get_content('stat_transformations', '1000+ Transformations'),
        'stat_satisfaction': get_content('stat_satisfaction', '98% Satisfaction'),
        'philosophie_titre': get_content('philosophie_titre', 'PLUS QU\'UNE SALLE, UN MODE DE VIE'),
        'philosophie_texte': get_content('philosophie_texte', 'Nous croyons en la discipline, la consistance et la communauté. Rejoins notre gang et transforme non seulement ton physique, mais aussi ton mindset. Ensemble, nous sommes plus forts.'),
        'cta_titre': get_content('cta_titre', 'PRÊT À COMMENCER TA TRANSFORMATION ?'),
        'cta_texte': get_content('cta_texte', 'Rejoins des milliers de membres qui ont déjà transformé leur vie avec FitGang.'),
        # Section programmes
        'prog_titre': get_content('hp_prog_titre', 'TROUVE TON PROGRAMME IDÉAL'),
        'prog_sous_titre': get_content('hp_prog_sous_titre', 'Que tu veux prendre du muscle, perdre du gras ou améliorer ta condition physique,<br>on a le programme qu\'il te faut.'),
        # Programme 1
        'prog1': {
            'badge': get_content('hp_prog1_badge', 'POPULAIRE'),
            'badge_color': get_content('hp_prog1_badge_color', 'bg-warning'),
            'titre': get_content('hp_prog1_titre', 'SÈCHE'),
            'description': get_content('hp_prog1_description', 'Perds du gras tout en préservant ta masse musculaire'),
            'features': get_content('hp_prog1_features', '12 semaines\nCardio HIIT\nPlan nutrition').split('\n'),
            'prix': get_content('hp_prog1_prix', '29€'),
            'image': get_content('hp_prog1_image', 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=600&h=800&fit=crop')
        },
        # Programme 2
        'prog2': {
            'badge': get_content('hp_prog2_badge', 'TOP VENTES'),
            'badge_color': get_content('hp_prog2_badge_color', 'bg-danger'),
            'titre': get_content('hp_prog2_titre', 'PRISE DE MASSE'),
            'description': get_content('hp_prog2_description', 'Construis du muscle de qualité avec notre méthode éprouvée'),
            'features': get_content('hp_prog2_features', '16 semaines\nHypertrophie\nCalories ++').split('\n'),
            'prix': get_content('hp_prog2_prix', '39€'),
            'image': get_content('hp_prog2_image', 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600&h=800&fit=crop')
        },
        # Programme 3
        'prog3': {
            'badge': get_content('hp_prog3_badge', ''),
            'badge_color': get_content('hp_prog3_badge_color', ''),
            'titre': get_content('hp_prog3_titre', 'FULL BODY'),
            'description': get_content('hp_prog3_description', 'Programme complet pour travailler tout le corps efficacement'),
            'features': get_content('hp_prog3_features', '8 semaines\n3x/semaine\nPolyvalent').split('\n'),
            'prix': get_content('hp_prog3_prix', '24€'),
            'image': get_content('hp_prog3_image', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&h=800&fit=crop')
        },
        # Programme 4
        'prog4': {
            'badge': get_content('hp_prog4_badge', 'DÉBUTANT'),
            'badge_color': get_content('hp_prog4_badge_color', 'bg-success'),
            'titre': get_content('hp_prog4_titre', 'DÉBUTANT'),
            'description': get_content('hp_prog4_description', 'Lance-toi dans le fitness avec des bases solides'),
            'features': get_content('hp_prog4_features', '6 semaines\nProgressif\nVidéos incluses').split('\n'),
            'prix': get_content('hp_prog4_prix', '19€'),
            'image': get_content('hp_prog4_image', 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&h=800&fit=crop')
        }
    }

    return render_template('index.html', programmes=programmes, ebooks=ebooks, page_content=page_content)


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

        # Envoyer un email de bienvenue
        try:
            email_sent = send_welcome_email(user)
            if email_sent:
                print(f"[INSCRIPTION] Email de bienvenue envoyé à {user.email}")
            else:
                print(f"[INSCRIPTION] ⚠️ Email de bienvenue NON envoyé à {user.email} - Vérifier config MAIL_*")
        except Exception as e:
            print(f"[INSCRIPTION] ✗ ERREUR lors de l'envoi de l'email de bienvenue: {e}")
            import traceback
            traceback.print_exc()

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

    # Récupérer toutes les séances organisées par semaine
    seances = ProgrammeSeance.query.filter_by(programme_id=id)\
        .order_by(ProgrammeSeance.semaine, ProgrammeSeance.jour).all()

    # Organiser par semaine
    seances_par_semaine = {}
    for seance in seances:
        if seance.semaine not in seances_par_semaine:
            seances_par_semaine[seance.semaine] = []
        seances_par_semaine[seance.semaine].append(seance)

    # Récupérer les séances complétées par l'utilisateur
    progressions = ProgrammeProgression.query.filter_by(user_id=current_user.id).all()
    seances_completees = {p.programme_seance_id for p in progressions if p.completed}

    # Calculer les stats de progression
    total_seances = len(seances)
    seances_completees_count = len(seances_completees)
    pourcentage_completion = (seances_completees_count / total_seances * 100) if total_seances > 0 else 0

    return render_template('programme_access.html',
                         programme=programme,
                         achat=achat,
                         seances_par_semaine=seances_par_semaine,
                         seances_completees=seances_completees,
                         total_seances=total_seances,
                         seances_completees_count=seances_completees_count,
                         pourcentage_completion=pourcentage_completion)


@bp.route('/programme/<int:prog_id>/seance/<int:seance_id>/toggle', methods=['POST'])
@login_required
def toggle_seance_completion(prog_id, seance_id):
    """Cocher/décocher une séance comme complétée"""
    # Vérifier que l'utilisateur a acheté le programme
    if not current_user.has_purchased(prog_id, 'programme'):
        return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403

    # Vérifier que la séance existe et appartient au programme
    seance = ProgrammeSeance.query.get_or_404(seance_id)
    if seance.programme_id != prog_id:
        return jsonify({'success': False, 'message': 'Séance non trouvée'}), 404

    # Chercher si la séance est déjà complétée
    progression = ProgrammeProgression.query.filter_by(
        user_id=current_user.id,
        programme_seance_id=seance_id
    ).first()

    if progression:
        # Toggle: si elle existe, on l'inverse ou la supprime
        if progression.completed:
            # Décocher
            db.session.delete(progression)
            completed = False
        else:
            # Cocher
            progression.completed = True
            progression.date_completed = datetime.utcnow()
            completed = True
    else:
        # Créer nouvelle progression
        progression = ProgrammeProgression(
            user_id=current_user.id,
            programme_seance_id=seance_id,
            completed=True,
            date_completed=datetime.utcnow()
        )
        db.session.add(progression)
        completed = True

    db.session.commit()

    return jsonify({'success': True, 'completed': completed})


@bp.route('/ebooks')
def ebooks():
    """Page listant tous les ebooks"""
    all_ebooks = Ebook.query.filter_by(actif=True).all()
    return render_template('ebooks.html', ebooks=all_ebooks)


@bp.route('/ebook/<int:id>')
def ebook_detail(id):
    """Page de détail d'un ebook spécifique"""
    ebook = Ebook.query.get_or_404(id)

    # Check if user has purchased this ebook
    has_purchased = False
    if current_user.is_authenticated:
        has_purchased = current_user.has_purchased(id, 'ebook')

    return render_template('ebook_detail.html', ebook=ebook, has_purchased=has_purchased)


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


# ===== ROUTES COMPLÉMENTS ALIMENTAIRES =====

@bp.route('/complements')
def complements():
    """Page listant tous les compléments alimentaires"""
    all_complements = Complement.query.filter_by(actif=True).order_by(Complement.categorie, Complement.nom).all()

    # Grouper par catégorie
    complements_par_categorie = {}
    for complement in all_complements:
        if complement.categorie not in complements_par_categorie:
            complements_par_categorie[complement.categorie] = []
        complements_par_categorie[complement.categorie].append(complement)

    return render_template('complements.html',
                         complements_par_categorie=complements_par_categorie)


@bp.route('/complement/<int:id>')
def complement_detail(id):
    """Page de détail d'un complément spécifique"""
    complement = Complement.query.get_or_404(id)

    # Check if user has purchased this complement
    has_purchased = False
    if current_user.is_authenticated:
        has_purchased = current_user.has_purchased(id, 'complement')

    return render_template('complement_detail.html', complement=complement, has_purchased=has_purchased)


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
    elif item_type == 'complement':
        item = Complement.query.get_or_404(item_id)
    else:
        flash('Type d\'article invalide.', 'danger')
        return redirect(url_for('main.index'))

    try:
        # Déterminer le nom du produit (titre pour programmes/ebooks, nom pour compléments)
        product_name = getattr(item, 'titre', None) or getattr(item, 'nom', 'Produit')

        # Créer une session Stripe Checkout
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': product_name,
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
        elif item_type == 'ebook':
            item = Ebook.query.get(item_id)
        elif item_type == 'complement':
            item = Complement.query.get(item_id)
        else:
            flash('Type d\'article invalide.', 'danger')
            return redirect(url_for('main.dashboard'))

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

        # Envoyer les emails
        try:
            # Email de confirmation au client
            email_client = send_purchase_confirmation_email(current_user, item, item_type)
            if email_client:
                print(f"[ACHAT] Email de confirmation envoyé à {current_user.email}")
            else:
                print(f"[ACHAT] ⚠️ Email de confirmation NON envoyé à {current_user.email} - Vérifier config MAIL_*")

            # Email de notification à l'admin
            admin_email = current_app.config.get('ADMIN_EMAIL')
            if admin_email:
                email_admin = send_admin_notification_email(admin_email, current_user, item, item_type)
                if email_admin:
                    print(f"[ACHAT] Email admin envoyé à {admin_email}")
                else:
                    print(f"[ACHAT] ⚠️ Email admin NON envoyé à {admin_email} - Vérifier config MAIL_*")
        except Exception as e:
            print(f"[ACHAT] ✗ ERREUR lors de l'envoi des emails: {e}")
            import traceback
            traceback.print_exc()

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

    # Statistiques de visiteurs / Analytics
    try:
        from app.analytics import get_visitor_stats
        visitor_stats = get_visitor_stats()
    except Exception as e:
        print(f"Erreur chargement stats visiteurs: {e}")
        visitor_stats = {
            'visitors_live': 0,
            'pageviews_live': 0,
            'visitors_today': 0,
            'pageviews_today': 0,
            'visitors_yesterday': 0,
            'visitors_week': 0,
            'visitors_month': 0,
            'top_pages_today': [],
            'visitors_trend': []
        }

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
                         achats_recents=achats_recents,
                         visitor_stats=visitor_stats)


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


# ===== ROUTES ADMIN - COMPLÉMENTS =====

@bp.route('/admin/complements')
@login_required
@admin_required
def admin_complements():
    """Liste des compléments alimentaires (admin)"""
    all_complements = Complement.query.order_by(Complement.date_creation.desc()).all()
    return render_template('admin_complements.html', complements=all_complements)


@bp.route('/admin/complement/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_complement():
    """Ajouter un complément"""
    form = ComplementForm()

    if form.validate_on_submit():
        complement = Complement(
            nom=form.nom.data,
            description=form.description.data,
            prix=form.prix.data,
            image=form.image.data,
            categorie=form.categorie.data,
            marque=form.marque.data,
            dosage=form.dosage.data,
            lien_achat=form.lien_achat.data,
            actif=form.actif.data
        )

        db.session.add(complement)
        db.session.commit()

        flash('Complément créé avec succès!', 'success')
        return redirect(url_for('main.admin_complements'))

    form.actif.data = True
    return render_template('admin_complement_form.html', form=form, title='Ajouter un complément')


@bp.route('/admin/complement/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_complement(id):
    """Modifier un complément"""
    complement = Complement.query.get_or_404(id)
    form = ComplementForm()

    if form.validate_on_submit():
        complement.nom = form.nom.data
        complement.description = form.description.data
        complement.prix = form.prix.data
        complement.image = form.image.data
        complement.categorie = form.categorie.data
        complement.marque = form.marque.data
        complement.dosage = form.dosage.data
        complement.lien_achat = form.lien_achat.data
        complement.actif = form.actif.data

        db.session.commit()

        flash('Complément mis à jour!', 'success')
        return redirect(url_for('main.admin_complements'))

    elif request.method == 'GET':
        form.nom.data = complement.nom
        form.description.data = complement.description
        form.prix.data = complement.prix
        form.image.data = complement.image
        form.categorie.data = complement.categorie
        form.marque.data = complement.marque
        form.dosage.data = complement.dosage
        form.lien_achat.data = complement.lien_achat
        form.actif.data = complement.actif

    return render_template('admin_complement_form.html', form=form, title='Modifier le complément', complement=complement)


@bp.route('/admin/complement/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_complement(id):
    """Supprimer un complément"""
    complement = Complement.query.get_or_404(id)

    db.session.delete(complement)
    db.session.commit()

    flash('Complément supprimé.', 'info')
    return redirect(url_for('main.admin_complements'))


@bp.route('/admin/homepage-content', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_homepage_content():
    """Gestion du contenu de la page d'accueil"""
    form = HomepageContentForm()

    if form.validate_on_submit():
        # Mise à jour de chaque section
        sections = {
            'hero_titre': form.hero_titre.data,
            'hero_sous_titre': form.hero_sous_titre.data,
            'stat_membres': form.stat_membres.data,
            'stat_programmes': form.stat_programmes.data,
            'stat_transformations': form.stat_transformations.data,
            'stat_satisfaction': form.stat_satisfaction.data,
            'philosophie_titre': form.philosophie_titre.data,
            'philosophie_texte': form.philosophie_texte.data,
            'cta_titre': form.cta_titre.data,
            'cta_texte': form.cta_texte.data
        }

        for section_key, contenu in sections.items():
            page_content = PageContent.query.filter_by(section=section_key).first()
            if page_content:
                page_content.contenu = contenu
                page_content.date_modification = datetime.utcnow()
            else:
                page_content = PageContent(section=section_key, contenu=contenu)
                db.session.add(page_content)

        db.session.commit()
        flash('Le contenu de la page d\'accueil a été mis à jour avec succès!', 'success')
        return redirect(url_for('main.admin_homepage_content'))

    # Pré-remplir le formulaire avec les valeurs actuelles
    if request.method == 'GET':
        form.hero_titre.data = PageContent.query.filter_by(section='hero_titre').first()
        form.hero_titre.data = form.hero_titre.data.contenu if form.hero_titre.data else ''

        content = PageContent.query.filter_by(section='hero_sous_titre').first()
        form.hero_sous_titre.data = content.contenu if content else ''

        content = PageContent.query.filter_by(section='stat_membres').first()
        form.stat_membres.data = content.contenu if content else ''

        content = PageContent.query.filter_by(section='stat_programmes').first()
        form.stat_programmes.data = content.contenu if content else ''

        content = PageContent.query.filter_by(section='stat_transformations').first()
        form.stat_transformations.data = content.contenu if content else ''

        content = PageContent.query.filter_by(section='stat_satisfaction').first()
        form.stat_satisfaction.data = content.contenu if content else ''

        content = PageContent.query.filter_by(section='philosophie_titre').first()
        form.philosophie_titre.data = content.contenu if content else ''

        content = PageContent.query.filter_by(section='philosophie_texte').first()
        form.philosophie_texte.data = content.contenu if content else ''

        content = PageContent.query.filter_by(section='cta_titre').first()
        form.cta_titre.data = content.contenu if content else ''

        content = PageContent.query.filter_by(section='cta_texte').first()
        form.cta_texte.data = content.contenu if content else ''

    return render_template('admin_homepage_content.html', form=form)


@bp.route('/admin/homepage-programmes', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_homepage_programmes():
    """Gestion de la section programmes de la page d'accueil"""
    form = HomepageProgrammesForm()

    if form.validate_on_submit():
        # Mise à jour de chaque section
        sections = {
            'hp_prog_titre': form.section_titre.data,
            'hp_prog_sous_titre': form.section_sous_titre.data,
            # Programme 1
            'hp_prog1_badge': form.prog1_badge.data or '',
            'hp_prog1_badge_color': form.prog1_badge_color.data or '',
            'hp_prog1_titre': form.prog1_titre.data,
            'hp_prog1_description': form.prog1_description.data,
            'hp_prog1_features': form.prog1_features.data,
            'hp_prog1_prix': form.prog1_prix.data,
            'hp_prog1_image': form.prog1_image.data,
            # Programme 2
            'hp_prog2_badge': form.prog2_badge.data or '',
            'hp_prog2_badge_color': form.prog2_badge_color.data or '',
            'hp_prog2_titre': form.prog2_titre.data,
            'hp_prog2_description': form.prog2_description.data,
            'hp_prog2_features': form.prog2_features.data,
            'hp_prog2_prix': form.prog2_prix.data,
            'hp_prog2_image': form.prog2_image.data,
            # Programme 3
            'hp_prog3_badge': form.prog3_badge.data or '',
            'hp_prog3_badge_color': form.prog3_badge_color.data or '',
            'hp_prog3_titre': form.prog3_titre.data,
            'hp_prog3_description': form.prog3_description.data,
            'hp_prog3_features': form.prog3_features.data,
            'hp_prog3_prix': form.prog3_prix.data,
            'hp_prog3_image': form.prog3_image.data,
            # Programme 4
            'hp_prog4_badge': form.prog4_badge.data or '',
            'hp_prog4_badge_color': form.prog4_badge_color.data or '',
            'hp_prog4_titre': form.prog4_titre.data,
            'hp_prog4_description': form.prog4_description.data,
            'hp_prog4_features': form.prog4_features.data,
            'hp_prog4_prix': form.prog4_prix.data,
            'hp_prog4_image': form.prog4_image.data,
        }

        for section_key, contenu in sections.items():
            page_content = PageContent.query.filter_by(section=section_key).first()
            if page_content:
                page_content.contenu = contenu
                page_content.date_modification = datetime.utcnow()
            else:
                page_content = PageContent(section=section_key, contenu=contenu)
                db.session.add(page_content)

        db.session.commit()
        flash('La section programmes de la page d\'accueil a été mise à jour avec succès!', 'success')
        return redirect(url_for('main.admin_homepage_programmes'))

    # Pré-remplir le formulaire avec les valeurs actuelles
    if request.method == 'GET':
        def get_content(section_name):
            content = PageContent.query.filter_by(section=section_name).first()
            return content.contenu if content else ''

        form.section_titre.data = get_content('hp_prog_titre') or 'TROUVE TON PROGRAMME IDÉAL'
        form.section_sous_titre.data = get_content('hp_prog_sous_titre') or 'Que tu veux prendre du muscle, perdre du gras ou améliorer ta condition physique,\non a le programme qu\'il te faut.'

        # Programme 1
        form.prog1_badge.data = get_content('hp_prog1_badge') or 'POPULAIRE'
        form.prog1_badge_color.data = get_content('hp_prog1_badge_color') or 'bg-warning'
        form.prog1_titre.data = get_content('hp_prog1_titre') or 'SÈCHE'
        form.prog1_description.data = get_content('hp_prog1_description') or 'Perds du gras tout en préservant ta masse musculaire'
        form.prog1_features.data = get_content('hp_prog1_features') or '12 semaines\nCardio HIIT\nPlan nutrition'
        form.prog1_prix.data = get_content('hp_prog1_prix') or '29€'
        form.prog1_image.data = get_content('hp_prog1_image') or 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=600&h=800&fit=crop'

        # Programme 2
        form.prog2_badge.data = get_content('hp_prog2_badge') or 'TOP VENTES'
        form.prog2_badge_color.data = get_content('hp_prog2_badge_color') or 'bg-danger'
        form.prog2_titre.data = get_content('hp_prog2_titre') or 'PRISE DE MASSE'
        form.prog2_description.data = get_content('hp_prog2_description') or 'Construis du muscle de qualité avec notre méthode éprouvée'
        form.prog2_features.data = get_content('hp_prog2_features') or '16 semaines\nHypertrophie\nCalories ++'
        form.prog2_prix.data = get_content('hp_prog2_prix') or '39€'
        form.prog2_image.data = get_content('hp_prog2_image') or 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600&h=800&fit=crop'

        # Programme 3
        form.prog3_badge.data = get_content('hp_prog3_badge') or ''
        form.prog3_badge_color.data = get_content('hp_prog3_badge_color') or ''
        form.prog3_titre.data = get_content('hp_prog3_titre') or 'FULL BODY'
        form.prog3_description.data = get_content('hp_prog3_description') or 'Programme complet pour travailler tout le corps efficacement'
        form.prog3_features.data = get_content('hp_prog3_features') or '8 semaines\n3x/semaine\nPolyvalent'
        form.prog3_prix.data = get_content('hp_prog3_prix') or '24€'
        form.prog3_image.data = get_content('hp_prog3_image') or 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&h=800&fit=crop'

        # Programme 4
        form.prog4_badge.data = get_content('hp_prog4_badge') or 'DÉBUTANT'
        form.prog4_badge_color.data = get_content('hp_prog4_badge_color') or 'bg-success'
        form.prog4_titre.data = get_content('hp_prog4_titre') or 'DÉBUTANT'
        form.prog4_description.data = get_content('hp_prog4_description') or 'Lance-toi dans le fitness avec des bases solides'
        form.prog4_features.data = get_content('hp_prog4_features') or '6 semaines\nProgressif\nVidéos incluses'
        form.prog4_prix.data = get_content('hp_prog4_prix') or '19€'
        form.prog4_image.data = get_content('hp_prog4_image') or 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&h=800&fit=crop'

    return render_template('admin_homepage_programmes.html', form=form)




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

    # Récupérer tous les programmes et ebooks (pour offrir)
    all_programmes = Programme.query.filter_by(actif=True).all()
    all_ebooks = Ebook.query.filter_by(actif=True).all()

    return render_template('admin_user_detail.html',
                         user=user,
                         achats=achats,
                         progressions=progressions,
                         total_depense=total_depense,
                         nb_progressions=nb_progressions,
                         all_programmes=all_programmes,
                         all_ebooks=all_ebooks)


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


@bp.route('/admin/user/<int:id>/reset-password', methods=['POST'])
@login_required
@admin_required
def admin_reset_password(id):
    """Réinitialiser le mot de passe d'un utilisateur"""
    user = User.query.get_or_404(id)

    new_password = request.form.get('new_password')

    if not new_password or len(new_password) < 6:
        flash('Le mot de passe doit contenir au moins 6 caractères.', 'danger')
        return redirect(url_for('main.admin_user_detail', id=id))

    user.set_password(new_password)
    db.session.commit()

    flash(f'Mot de passe de {user.prenom} {user.nom} réinitialisé avec succès.', 'success')
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


@bp.route('/admin/user/<int:id>/grant-access', methods=['POST'])
@login_required
@admin_required
def admin_grant_access(id):
    """Donner accès gratuit à un programme ou ebook à un utilisateur"""
    user = User.query.get_or_404(id)

    item_type = request.form.get('item_type')  # 'programme' ou 'ebook'
    item_id = request.form.get('item_id')

    if not item_type or not item_id:
        flash('Informations manquantes.', 'danger')
        return redirect(url_for('main.admin_user_detail', id=id))

    # Vérifier si l'utilisateur a déjà cet article
    existing = Achat.query.filter_by(
        user_id=user.id,
        item_id=item_id,
        type=item_type
    ).first()

    if existing:
        flash('L\'utilisateur possède déjà cet article.', 'warning')
        return redirect(url_for('main.admin_user_detail', id=id))

    # Récupérer l'article
    if item_type == 'programme':
        item = Programme.query.get_or_404(item_id)
    else:
        item = Ebook.query.get_or_404(item_id)

    # Créer l'achat gratuit (prix = 0)
    achat = Achat(
        user_id=user.id,
        item_id=item_id,
        type=item_type,
        prix_paye=0.0,  # Gratuit
        stripe_session_id=f'admin_grant_{secrets.token_hex(8)}'
    )

    db.session.add(achat)
    db.session.commit()

    flash(f'{item.titre} offert à {user.prenom} {user.nom} avec succès!', 'success')
    return redirect(url_for('main.admin_user_detail', id=id))


@bp.route('/admin/transformations')
@login_required
@admin_required
def admin_transformations():
    """Page admin pour voir toutes les transformations des utilisateurs"""
    # Récupérer tous les utilisateurs qui ont au moins une photo
    users_with_photos = db.session.query(User)\
        .join(Photo, User.id == Photo.user_id)\
        .distinct()\
        .all()

    transformations = []

    for user in users_with_photos:
        # Récupérer la première photo "avant" et la dernière photo "après"
        photo_avant = Photo.query.filter_by(user_id=user.id, type='avant')\
            .order_by(Photo.date_upload.asc()).first()
        photo_apres = Photo.query.filter_by(user_id=user.id, type='apres')\
            .order_by(Photo.date_upload.desc()).first()

        if photo_avant and photo_apres:
            # Calculer la différence de poids
            poids_diff = None
            if photo_avant.poids and photo_apres.poids:
                poids_diff = photo_apres.poids - photo_avant.poids

            # Calculer la durée de transformation
            duree_jours = (photo_apres.date_upload - photo_avant.date_upload).days

            transformations.append({
                'user': user,
                'photo_avant': photo_avant,
                'photo_apres': photo_apres,
                'poids_diff': poids_diff,
                'duree_jours': duree_jours,
                'nb_photos_avant': Photo.query.filter_by(user_id=user.id, type='avant').count(),
                'nb_photos_apres': Photo.query.filter_by(user_id=user.id, type='apres').count()
            })

    # Trier par date la plus récente
    transformations.sort(key=lambda x: x['photo_apres'].date_upload, reverse=True)

    return render_template('admin_transformations.html', transformations=transformations)


@bp.route('/admin/photo/<int:id>/toggle-public', methods=['POST'])
@login_required
@admin_required
def admin_toggle_photo_public(id):
    """Basculer la visibilité publique d'une photo (pour témoignages)"""
    photo = Photo.query.get_or_404(id)

    photo.visible_public = not photo.visible_public
    db.session.commit()

    status = "publique" if photo.visible_public else "privée"
    flash(f'Photo marquée comme {status}.', 'success')

    return redirect(url_for('main.admin_transformations'))


# ===== ROUTES ADMIN SÉANCES DE PROGRAMME =====

@bp.route('/admin/programme/<int:id>/seances')
@login_required
@admin_required
def admin_programme_seances(id):
    """Liste des séances d'un programme"""
    programme = Programme.query.get_or_404(id)

    # Récupérer toutes les séances organisées par semaine et jour
    seances = ProgrammeSeance.query.filter_by(programme_id=id)\
        .order_by(ProgrammeSeance.semaine, ProgrammeSeance.jour).all()

    # Organiser par semaine
    seances_par_semaine = {}
    for seance in seances:
        if seance.semaine not in seances_par_semaine:
            seances_par_semaine[seance.semaine] = []
        seances_par_semaine[seance.semaine].append(seance)

    return render_template('admin_programme_seances.html',
                         programme=programme,
                         seances_par_semaine=seances_par_semaine)


@bp.route('/admin/programme/<int:id>/seance/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_seance(id):
    """Ajouter une séance à un programme"""
    programme = Programme.query.get_or_404(id)
    form = SeanceForm()

    if form.validate_on_submit():
        seance = ProgrammeSeance(
            programme_id=id,
            semaine=form.semaine.data,
            jour=form.jour.data,
            titre=form.titre.data,
            exercices=form.exercices.data,
            notes=form.notes.data,
            ordre=(form.semaine.data - 1) * 7 + form.jour.data
        )

        db.session.add(seance)
        db.session.commit()

        flash(f'Séance "{seance.titre}" ajoutée avec succès!', 'success')
        return redirect(url_for('main.admin_programme_seances', id=id))

    return render_template('admin_seance_form.html',
                         form=form,
                         programme=programme,
                         title='Ajouter une séance')


@bp.route('/admin/programme/<int:prog_id>/seance/<int:seance_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_seance(prog_id, seance_id):
    """Modifier une séance"""
    programme = Programme.query.get_or_404(prog_id)
    seance = ProgrammeSeance.query.get_or_404(seance_id)

    # Vérifier que la séance appartient bien au programme
    if seance.programme_id != prog_id:
        flash('Séance non trouvée.', 'danger')
        return redirect(url_for('main.admin_programme_seances', id=prog_id))

    form = SeanceForm()

    if form.validate_on_submit():
        seance.semaine = form.semaine.data
        seance.jour = form.jour.data
        seance.titre = form.titre.data
        seance.exercices = form.exercices.data
        seance.notes = form.notes.data
        seance.ordre = (form.semaine.data - 1) * 7 + form.jour.data

        db.session.commit()

        flash('Séance mise à jour!', 'success')
        return redirect(url_for('main.admin_programme_seances', id=prog_id))

    elif request.method == 'GET':
        form.semaine.data = seance.semaine
        form.jour.data = seance.jour
        form.titre.data = seance.titre
        form.exercices.data = seance.exercices
        form.notes.data = seance.notes

    return render_template('admin_seance_form.html',
                         form=form,
                         programme=programme,
                         seance=seance,
                         title='Modifier la séance')


@bp.route('/admin/programme/<int:prog_id>/seance/<int:seance_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_seance(prog_id, seance_id):
    """Supprimer une séance"""
    seance = ProgrammeSeance.query.get_or_404(seance_id)

    # Vérifier que la séance appartient bien au programme
    if seance.programme_id != prog_id:
        flash('Séance non trouvée.', 'danger')
        return redirect(url_for('main.admin_programme_seances', id=prog_id))

    db.session.delete(seance)
    db.session.commit()

    flash('Séance supprimée.', 'info')
    return redirect(url_for('main.admin_programme_seances', id=prog_id))


# ===== ROUTES PHOTOS =====

@bp.route('/photos')
@login_required
def photos():
    """Page de gestion des photos avant/après"""
    photos_avant = Photo.query.filter_by(user_id=current_user.id, type='avant')\
        .order_by(Photo.date_upload.desc()).all()
    photos_apres = Photo.query.filter_by(user_id=current_user.id, type='apres')\
        .order_by(Photo.date_upload.desc()).all()

    return render_template('photos.html',
                         photos_avant=photos_avant,
                         photos_apres=photos_apres)


@bp.route('/photo/upload', methods=['POST'])
@login_required
def upload_photo():
    """Upload d'une photo de transformation"""
    if 'photo' not in request.files:
        flash('Aucune photo sélectionnée.', 'danger')
        return redirect(url_for('main.photos'))

    file = request.files['photo']
    if file.filename == '':
        flash('Aucune photo sélectionnée.', 'danger')
        return redirect(url_for('main.photos'))

    # Vérifier l'extension du fichier
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    if '.' not in file.filename or \
       file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        flash('Format de fichier non autorisé. Utilisez: PNG, JPG, JPEG, GIF, WEBP', 'danger')
        return redirect(url_for('main.photos'))

    # Générer un nom de fichier unique
    random_hex = secrets.token_hex(16)
    _, file_ext = os.path.splitext(secure_filename(file.filename))
    filename = f"photo_{current_user.id}_{random_hex}{file_ext}"

    # Sauvegarder le fichier
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # Créer l'entrée en base de données
    photo = Photo(
        user_id=current_user.id,
        fichier=filename,
        type=request.form.get('type', 'avant'),
        poids=request.form.get('poids') if request.form.get('poids') else None,
        notes=request.form.get('notes', ''),
        visible_public=False
    )

    db.session.add(photo)
    db.session.commit()

    flash('Photo ajoutée avec succès!', 'success')
    return redirect(url_for('main.photos'))


@bp.route('/photo/<int:id>/delete', methods=['POST'])
@login_required
def delete_photo(id):
    """Supprimer une photo"""
    photo = Photo.query.get_or_404(id)

    # Vérifier que la photo appartient bien à l'utilisateur
    if photo.user_id != current_user.id and not current_user.is_admin:
        flash('Vous ne pouvez pas supprimer cette photo.', 'danger')
        return redirect(url_for('main.photos'))

    # Supprimer le fichier physique
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
    file_path = os.path.join(upload_folder, photo.fichier)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Supprimer l'entrée en base de données
    db.session.delete(photo)
    db.session.commit()

    flash('Photo supprimée.', 'info')
    return redirect(url_for('main.photos'))


@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """Servir les fichiers uploadés"""
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
    return send_from_directory(upload_folder, filename)


# ===== ROUTES STATISTIQUES =====

@bp.route('/statistiques')
@login_required
def statistiques():
    """Page de statistiques et graphiques de progression"""
    # Récupérer toutes les progressions de l'utilisateur
    progressions = Progression.query.filter_by(user_id=current_user.id)\
        .order_by(Progression.date.asc()).all()

    # Préparer les données pour les graphiques
    dates = []
    poids_data = []
    seances_count = {}

    for prog in progressions:
        dates.append(prog.date.strftime('%Y-%m-%d'))
        if prog.poids:
            poids_data.append(prog.poids)

        # Compter les séances
        if prog.seance:
            seances_count[prog.seance] = seances_count.get(prog.seance, 0) + 1

    # Calculer quelques stats
    nb_seances = len(progressions)
    seances_last_30_days = Progression.query.filter(
        Progression.user_id == current_user.id,
        Progression.date >= datetime.utcnow() - timedelta(days=30)
    ).count()

    # Poids initial et actuel
    poids_initial = poids_data[0] if poids_data else None
    poids_actuel = poids_data[-1] if poids_data else None
    poids_diff = (poids_actuel - poids_initial) if (poids_initial and poids_actuel) else None

    return render_template('statistiques.html',
                         progressions=progressions,
                         dates=dates,
                         poids_data=poids_data,
                         seances_count=seances_count,
                         nb_seances=nb_seances,
                         seances_last_30_days=seances_last_30_days,
                         poids_initial=poids_initial,
                         poids_actuel=poids_actuel,
                         poids_diff=poids_diff)


# ===== ROUTES OUTILS / CALCULATEURS =====

@bp.route('/calculateurs')
@login_required
def calculateurs():
    """Page des calculateurs fitness (IMC, calories, macros, 1RM)"""
    return render_template('calculateurs.html')


# ===== ROUTES NEWSLETTER =====

@bp.route('/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    """S'abonner à la newsletter"""
    email = request.form.get('email') or (request.json.get('email') if request.is_json else None)

    if not email:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Email requis'}), 400
        flash('Email requis', 'danger')
        return redirect(url_for('main.index'))

    # Vérifier si l'email est déjà abonné
    existing = Newsletter.query.filter_by(email=email).first()

    if existing:
        if existing.actif:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Cet email est déjà abonné'})
            flash('Cet email est déjà abonné à la newsletter', 'info')
        else:
            # Réactiver l'abonnement
            existing.actif = True
            existing.date_inscription = datetime.utcnow()
            db.session.commit()
            if request.is_json:
                return jsonify({'success': True, 'message': 'Abonnement réactivé avec succès!'})
            flash('Ton abonnement a été réactivé!', 'success')
    else:
        # Créer un nouvel abonnement
        newsletter = Newsletter(email=email)
        db.session.add(newsletter)
        db.session.commit()

        if request.is_json:
            return jsonify({'success': True, 'message': 'Merci de ton abonnement!'})
        flash('Merci de t\'être abonné à notre newsletter!', 'success')

    return redirect(url_for('main.index'))


@bp.route('/admin/newsletter')
@login_required
@admin_required
def admin_newsletter():
    """Liste des abonnés à la newsletter (admin)"""
    abonnes = Newsletter.query.filter_by(actif=True).order_by(Newsletter.date_inscription.desc()).all()
    total_abonnes = Newsletter.query.filter_by(actif=True).count()
    return render_template('admin_newsletter.html', abonnes=abonnes, total_abonnes=total_abonnes)


@bp.route('/admin/newsletter/import', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_newsletter_import():
    """Import d'emails en masse via CSV"""
    form = EmailImportForm()
    if form.validate_on_submit():
        try:
            import re
            file = form.fichier_csv.data
            # Lire le fichier
            content = file.read().decode('utf-8')
            emails = []

            # Parser le CSV (un email par ligne)
            for line in content.split('\n'):
                line = line.strip()
                if line and '@' in line:
                    # Détection du séparateur: , ou ;
                    separator = ';' if ';' in line else ','

                    # Extraire seulement l'email (première partie avant le séparateur)
                    if separator in line:
                        parts = line.split(separator)
                        email = parts[0].strip().strip('"')
                    else:
                        email = line.strip()

                    # Utiliser regex pour extraire un email valide
                    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', email)
                    if email_match:
                        clean_email = email_match.group(0).lower()
                        emails.append(clean_email)

            # Ajouter les emails à la base de données
            added = 0
            duplicates = 0
            for email in set(emails):  # set() pour éviter les doublons dans le fichier
                existing = Newsletter.query.filter_by(email=email).first()
                if existing:
                    if not existing.actif:
                        existing.actif = True
                        added += 1
                    else:
                        duplicates += 1
                else:
                    newsletter = Newsletter(email=email)
                    db.session.add(newsletter)
                    added += 1

            db.session.commit()
            flash(f'{added} emails importés avec succès! ({duplicates} doublons ignorés)', 'success')
            return redirect(url_for('main.admin_newsletter'))

        except Exception as e:
            flash(f'Erreur lors de l\'import: {str(e)}', 'danger')

    return render_template('admin_newsletter_import.html', form=form)


@bp.route('/admin/newsletter/cleanup', methods=['POST'])
@login_required
@admin_required
def admin_newsletter_cleanup():
    """Nettoyer les emails mal formatés dans la base de données"""
    import re

    try:
        all_subscribers = Newsletter.query.all()
        cleaned = 0
        deleted = 0

        for subscriber in all_subscribers:
            # Extraire l'email valide avec regex
            email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', subscriber.email)

            if email_match:
                clean_email = email_match.group(0).lower()
                if clean_email != subscriber.email:
                    # Vérifier si l'email nettoyé existe déjà
                    existing = Newsletter.query.filter_by(email=clean_email).filter(Newsletter.id != subscriber.id).first()
                    if existing:
                        # Supprimer le doublon mal formaté
                        db.session.delete(subscriber)
                        deleted += 1
                    else:
                        # Nettoyer l'email
                        subscriber.email = clean_email
                        cleaned += 1
            else:
                # Pas d'email valide trouvé, supprimer l'entrée
                db.session.delete(subscriber)
                deleted += 1

        db.session.commit()
        flash(f'{cleaned} emails nettoyés, {deleted} entrées invalides supprimées!', 'success')
    except Exception as e:
        flash(f'Erreur lors du nettoyage: {str(e)}', 'danger')

    return redirect(url_for('main.admin_newsletter'))


@bp.route('/admin/newsletter/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_newsletter_delete(id):
    """Supprimer un abonné"""
    subscriber = Newsletter.query.get_or_404(id)
    email = subscriber.email
    db.session.delete(subscriber)
    db.session.commit()
    flash(f'Abonné {email} supprimé!', 'info')
    return redirect(url_for('main.admin_newsletter'))


@bp.route('/admin/email-campaigns')
@login_required
@admin_required
def admin_email_campaigns():
    """Liste des campagnes d'emails"""
    campaigns = EmailCampaign.query.order_by(EmailCampaign.date_creation.desc()).all()
    total_subscribers = Newsletter.query.filter_by(actif=True).count()
    return render_template('admin_email_campaigns.html', campaigns=campaigns, total_subscribers=total_subscribers)


@bp.route('/admin/email-campaigns/create', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_email_campaign_create():
    """Créer une nouvelle campagne d'email"""
    form = EmailCampaignForm()
    if form.validate_on_submit():
        campaign = EmailCampaign(
            nom=form.nom.data,
            sujet=form.sujet.data,
            contenu_html=form.contenu_html.data,
            contenu_texte=form.contenu_texte.data,
            created_by_user_id=current_user.id,
            statut='brouillon'
        )
        db.session.add(campaign)
        db.session.commit()
        flash('Campagne créée avec succès!', 'success')
        return redirect(url_for('main.admin_email_campaign_detail', id=campaign.id))

    return render_template('admin_email_campaign_form.html', form=form, title='Créer une campagne d\'email')


@bp.route('/admin/email-campaigns/<int:id>')
@login_required
@admin_required
def admin_email_campaign_detail(id):
    """Détails d'une campagne d'email"""
    campaign = EmailCampaign.query.get_or_404(id)
    preview_emails = preview_campaign_recipients(id, limit=10)
    total_subscribers = Newsletter.query.filter_by(actif=True).count()
    return render_template('admin_email_campaign_detail.html',
                         campaign=campaign,
                         preview_emails=preview_emails,
                         total_subscribers=total_subscribers)


@bp.route('/admin/email-campaigns/<int:id>/test', methods=['POST'])
@login_required
@admin_required
def admin_email_campaign_test(id):
    """Envoyer un email de test"""
    campaign = EmailCampaign.query.get_or_404(id)
    test_email = request.form.get('test_email', current_user.email)

    try:
        text_body = campaign.contenu_texte or campaign.contenu_html.replace('<br>', '\n')
        success = send_test_email(test_email, campaign.sujet, campaign.contenu_html, text_body)

        if success:
            flash(f'Email de test envoyé avec succès à {test_email}!', 'success')
        else:
            flash(f'Erreur lors de l\'envoi de l\'email de test. Vérifiez la configuration SMTP.', 'warning')
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'danger')

    return redirect(url_for('main.admin_email_campaign_detail', id=id))


@bp.route('/admin/email-campaigns/<int:id>/send', methods=['POST'])
@login_required
@admin_required
def admin_email_campaign_send(id):
    """Lancer l'envoi en masse d'une campagne"""
    campaign = EmailCampaign.query.get_or_404(id)

    if campaign.statut == 'en_cours':
        flash('Cette campagne est déjà en cours d\'envoi!', 'warning')
        return redirect(url_for('main.admin_email_campaign_detail', id=id))

    if campaign.statut == 'terminee':
        flash('Cette campagne a déjà été envoyée!', 'info')
        return redirect(url_for('main.admin_email_campaign_detail', id=id))

    try:
        # Lancer l'envoi en arrière-plan (pour un vrai serveur, utiliser Celery ou RQ)
        # Pour l'instant, on lance de manière synchrone avec un petit batch
        stats = send_bulk_emails(campaign.id, batch_size=50, delay_between_batches=2)

        flash(f'Campagne envoyée! {stats["sent"]} emails envoyés, {stats["errors"]} erreurs sur {stats["total"]} destinataires.', 'success')
    except Exception as e:
        flash(f'Erreur lors du lancement de la campagne: {str(e)}', 'danger')

    return redirect(url_for('main.admin_email_campaign_detail', id=id))


@bp.route('/admin/email-campaigns/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_email_campaign_delete(id):
    """Supprimer une campagne d'email"""
    campaign = EmailCampaign.query.get_or_404(id)

    if campaign.statut == 'en_cours':
        flash('Impossible de supprimer une campagne en cours d\'envoi!', 'danger')
        return redirect(url_for('main.admin_email_campaign_detail', id=id))

    db.session.delete(campaign)
    db.session.commit()
    flash('Campagne supprimée avec succès!', 'info')
    return redirect(url_for('main.admin_email_campaigns'))
