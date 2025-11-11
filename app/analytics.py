"""
Module de tracking et analytics pour FitGang
Enregistre les visites et fournit des statistiques
"""
from datetime import datetime, timedelta
from flask import request, session
from flask_login import current_user
from app import db
from sqlalchemy import func
import uuid


def check_visits_table_exists():
    """Vérifie si la table visits existe dans la DB"""
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        return 'visits' in inspector.get_table_names()
    except:
        return False


def track_visit():
    """
    Enregistre une visite dans la base de données
    Appelé automatiquement via before_request
    """
    try:
        # Vérifier si la table visits existe
        if not check_visits_table_exists():
            return

        # Import ici pour éviter les erreurs si la table n'existe pas
        from app.models import Visit

        # Ne pas tracker les requêtes statiques et AJAX
        if request.endpoint and (
            request.endpoint.startswith('static') or
            request.is_json or
            request.path.startswith('/static/')
        ):
            return

        # Générer ou récupérer l'ID de session
        if 'visitor_session_id' not in session:
            session['visitor_session_id'] = str(uuid.uuid4())

        # Créer l'enregistrement de visite
        visit = Visit(
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:500],
            page=request.path[:500],
            referer=request.referrer[:500] if request.referrer else None,
            user_id=current_user.id if current_user.is_authenticated else None,
            session_id=session['visitor_session_id']
        )

        db.session.add(visit)
        db.session.commit()

    except Exception as e:
        # En cas d'erreur, ne pas bloquer la requête
        print(f"Erreur tracking visite: {e}")
        db.session.rollback()


def get_visitor_stats():
    """
    Récupère les statistiques de visiteurs
    Retourne un dictionnaire avec les stats
    """
    # Vérifier si la table visits existe
    if not check_visits_table_exists():
        return {
            'visitors_live': 0,
            'pageviews_live': 0,
            'visitors_today': 0,
            'pageviews_today': 0,
            'visitors_yesterday': 0,
            'pageviews_yesterday': 0,
            'visitors_week': 0,
            'pageviews_week': 0,
            'visitors_month': 0,
            'pageviews_month': 0,
            'visitors_total': 0,
            'pageviews_total': 0,
            'top_pages_today': [],
            'top_referers_today': [],
            'visitors_trend': []
        }

    # Import ici pour éviter les erreurs si la table n'existe pas
    from app.models import Visit

    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    yesterday_start = today_start - timedelta(days=1)
    week_start = now - timedelta(days=7)
    month_start = datetime(now.year, now.month, 1)

    # 15 dernières minutes = en direct
    live_threshold = now - timedelta(minutes=15)

    stats = {}

    # Visiteurs en direct (15 dernières minutes) - sessions uniques
    stats['visitors_live'] = Visit.query.filter(
        Visit.timestamp >= live_threshold
    ).distinct(Visit.session_id).count()

    # Vues de pages en direct
    stats['pageviews_live'] = Visit.query.filter(
        Visit.timestamp >= live_threshold
    ).count()

    # Aujourd'hui - visiteurs uniques (par session)
    stats['visitors_today'] = Visit.query.filter(
        Visit.timestamp >= today_start
    ).distinct(Visit.session_id).count()

    # Aujourd'hui - vues de pages
    stats['pageviews_today'] = Visit.query.filter(
        Visit.timestamp >= today_start
    ).count()

    # Hier
    stats['visitors_yesterday'] = Visit.query.filter(
        Visit.timestamp >= yesterday_start,
        Visit.timestamp < today_start
    ).distinct(Visit.session_id).count()

    stats['pageviews_yesterday'] = Visit.query.filter(
        Visit.timestamp >= yesterday_start,
        Visit.timestamp < today_start
    ).count()

    # Cette semaine
    stats['visitors_week'] = Visit.query.filter(
        Visit.timestamp >= week_start
    ).distinct(Visit.session_id).count()

    stats['pageviews_week'] = Visit.query.filter(
        Visit.timestamp >= week_start
    ).count()

    # Ce mois
    stats['visitors_month'] = Visit.query.filter(
        Visit.timestamp >= month_start
    ).distinct(Visit.session_id).count()

    stats['pageviews_month'] = Visit.query.filter(
        Visit.timestamp >= month_start
    ).count()

    # Total (all time)
    stats['visitors_total'] = Visit.query.distinct(Visit.session_id).count()
    stats['pageviews_total'] = Visit.query.count()

    # Pages les plus visitées aujourd'hui (top 5)
    stats['top_pages_today'] = db.session.query(
        Visit.page,
        func.count(Visit.id).label('count')
    ).filter(
        Visit.timestamp >= today_start
    ).group_by(Visit.page).order_by(
        func.count(Visit.id).desc()
    ).limit(5).all()

    # Sources de trafic aujourd'hui (top 5 referers)
    stats['top_referers_today'] = db.session.query(
        Visit.referer,
        func.count(Visit.id).label('count')
    ).filter(
        Visit.timestamp >= today_start,
        Visit.referer.isnot(None),
        Visit.referer != ''
    ).group_by(Visit.referer).order_by(
        func.count(Visit.id).desc()
    ).limit(5).all()

    # Évolution des visiteurs (7 derniers jours)
    stats['visitors_trend'] = []
    for i in range(7):
        day_start = today_start - timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        count = Visit.query.filter(
            Visit.timestamp >= day_start,
            Visit.timestamp < day_end
        ).distinct(Visit.session_id).count()
        stats['visitors_trend'].insert(0, {
            'date': day_start.strftime('%d/%m'),
            'count': count
        })

    return stats


def get_hourly_stats_today():
    """
    Retourne les stats par heure pour aujourd'hui
    Utile pour voir les pics d'activité
    """
    # Vérifier si la table visits existe
    if not check_visits_table_exists():
        return []

    # Import ici pour éviter les erreurs si la table n'existe pas
    from app.models import Visit

    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)

    hourly_stats = []
    for hour in range(24):
        hour_start = today_start + timedelta(hours=hour)
        hour_end = hour_start + timedelta(hours=1)

        count = Visit.query.filter(
            Visit.timestamp >= hour_start,
            Visit.timestamp < hour_end
        ).count()

        hourly_stats.append({
            'hour': f'{hour:02d}h',
            'count': count
        })

    return hourly_stats


def cleanup_old_visits(days=90):
    """
    Nettoie les anciennes visites pour ne pas surcharger la DB
    Par défaut, garde 90 jours d'historique
    """
    # Vérifier si la table visits existe
    if not check_visits_table_exists():
        return 0

    # Import ici pour éviter les erreurs si la table n'existe pas
    from app.models import Visit

    cutoff_date = datetime.utcnow() - timedelta(days=days)

    try:
        deleted = Visit.query.filter(Visit.timestamp < cutoff_date).delete()
        db.session.commit()
        return deleted
    except Exception as e:
        print(f"Erreur nettoyage visites: {e}")
        db.session.rollback()
        return 0
