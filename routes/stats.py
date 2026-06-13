from flask import Blueprint, jsonify, session, request
from datetime import date, timedelta
from sqlalchemy import func
from models import db
from models.checkin import Checkin
from models.ability import Ability

bp = Blueprint('stats', __name__, url_prefix='/api/stats')

@bp.route('/summary', methods=['GET'])
def get_summary():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    total_checkins = Checkin.query.filter_by(user_id=user_id).count()

    from services.exp_service import ExpService
    streak = ExpService.get_current_streak(user_id)

    ability_counts = db.session.query(
        Ability.name,
        func.count(Checkin.id).label('count')
    ).join(Checkin).filter(
        Checkin.user_id == user_id
    ).group_by(Ability.id).order_by(func.count(Checkin.id).desc()).all()

    top_ability = ability_counts[0] if ability_counts else ('无', 0)

    today_count = Checkin.query.filter_by(
        user_id=user_id,
        checkin_date=date.today()
    ).count()

    week_start = date.today() - timedelta(days=6)
    week_count = Checkin.query.filter(
        Checkin.user_id == user_id,
        Checkin.checkin_date >= week_start
    ).count()

    return jsonify({
        'total_checkins': total_checkins,
        'current_streak': streak,
        'today_checkins': today_count,
        'week_checkins': week_count,
        'top_ability': {
            'name': top_ability[0],
            'count': top_ability[1]
        },
        'ability_distribution': [
            {'name': name, 'count': count}
            for name, count in ability_counts
        ]
    })

@bp.route('/weekly', methods=['GET'])
def weekly_stats():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    end_date = date.today()
    start_date = end_date - timedelta(days=6)

    daily_counts = db.session.query(
        Checkin.checkin_date,
        func.count(Checkin.id).label('count')
    ).filter(
        Checkin.user_id == user_id,
        Checkin.checkin_date >= start_date,
        Checkin.checkin_date <= end_date
    ).group_by(Checkin.checkin_date).all()

    ability_counts = db.session.query(
        Ability.name,
        Ability.color,
        func.count(Checkin.id).label('count')
    ).join(Checkin).filter(
        Checkin.user_id == user_id,
        Checkin.checkin_date >= start_date
    ).group_by(Ability.id).all()

    date_counts = {d: c for d, c in daily_counts}
    daily_data = []
    current = start_date
    while current <= end_date:
        daily_data.append({
            'date': current.isoformat(),
            'count': date_counts.get(current, 0)
        })
        current += timedelta(days=1)

    return jsonify({
        'period': {
            'start': start_date.isoformat(),
            'end': end_date.isoformat()
        },
        'daily_counts': daily_data,
        'ability_counts': [
            {'name': name, 'color': color, 'count': count}
            for name, color, count in ability_counts
        ],
        'total_checkins': sum(c for _, c in daily_counts)
    })

@bp.route('/monthly', methods=['GET'])
def monthly_stats():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    year = request.args.get('year', date.today().year, type=int)
    month = request.args.get('month', date.today().month, type=int)

    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)

    daily_counts = db.session.query(
        Checkin.checkin_date,
        func.count(Checkin.id).label('count')
    ).filter(
        Checkin.user_id == user_id,
        Checkin.checkin_date >= start_date,
        Checkin.checkin_date <= end_date
    ).group_by(Checkin.checkin_date).all()

    ability_counts = db.session.query(
        Ability.name,
        Ability.color,
        func.count(Checkin.id).label('count')
    ).join(Checkin).filter(
        Checkin.user_id == user_id,
        Checkin.checkin_date >= start_date,
        Checkin.checkin_date <= end_date
    ).group_by(Ability.id).all()

    return jsonify({
        'period': {
            'year': year,
            'month': month,
            'start': start_date.isoformat(),
            'end': end_date.isoformat()
        },
        'daily_counts': [
            {'date': d.isoformat(), 'count': c}
            for d, c in daily_counts
        ],
        'ability_counts': [
            {'name': name, 'color': color, 'count': count}
            for name, color, count in ability_counts
        ],
        'total_checkins': sum(c for _, c in daily_counts)
    })

@bp.route('/yearly', methods=['GET'])
def yearly_stats():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    year = request.args.get('year', date.today().year, type=int)

    monthly_counts = []
    for month in range(1, 13):
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)

        count = Checkin.query.filter(
            Checkin.user_id == user_id,
            Checkin.checkin_date >= start_date,
            Checkin.checkin_date <= end_date
        ).count()

        monthly_counts.append({
            'month': month,
            'count': count
        })

    ability_counts = db.session.query(
        Ability.name,
        Ability.color,
        func.count(Checkin.id).label('count')
    ).join(Checkin).filter(
        Checkin.user_id == user_id,
        db.extract('year', Checkin.checkin_date) == year
    ).group_by(Ability.id).all()

    return jsonify({
        'year': year,
        'monthly_counts': monthly_counts,
        'ability_counts': [
            {'name': name, 'color': color, 'count': count}
            for name, color, count in ability_counts
        ],
        'total_checkins': sum(m['count'] for m in monthly_counts)
    })
