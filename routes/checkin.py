from flask import Blueprint, request, jsonify, session
from datetime import date, timedelta
from models import db
from models.checkin import Checkin
from models.ability import UserAbility, Ability
from models.user import User
from services.exp_service import ExpService
from services.achievement_service import AchievementService

bp = Blueprint('checkin', __name__, url_prefix='/api/checkin')

@bp.route('/today', methods=['GET'])
def get_today_checkins():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    today = date.today()

    checkins = Checkin.query.filter_by(
        user_id=user_id,
        checkin_date=today
    ).all()

    checked_abilities = [c.ability_id for c in checkins]

    streak = ExpService.get_current_streak(user_id)

    return jsonify({
        'date': today.isoformat(),
        'checked_abilities': checked_abilities,
        'total_today': len(checkins),
        'streak': streak
    })

@bp.route('', methods=['POST'])
def create_checkin():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    data = request.get_json()
    ability_id = data.get('ability_id')
    note = data.get('note', '')
    mood = data.get('mood')

    if not ability_id:
        return jsonify({'error': '缺少能力ID'}), 400

    today = date.today()

    existing = Checkin.query.filter_by(
        user_id=user_id,
        ability_id=ability_id,
        checkin_date=today
    ).first()

    if existing:
        return jsonify({'error': '今日已打卡'}), 400

    exp = ExpService.calculate_exp(user_id, ability_id)

    checkin = Checkin(
        user_id=user_id,
        ability_id=ability_id,
        checkin_date=today,
        exp_gained=exp,
        note=note,
        mood=mood
    )
    db.session.add(checkin)

    user_ability = UserAbility.query.filter_by(
        user_id=user_id,
        ability_id=ability_id
    ).first()

    if not user_ability:
        user_ability = UserAbility(
            user_id=user_id,
            ability_id=ability_id,
            current_value=0,
            total_checkins=0
        )
        db.session.add(user_ability)

    user_ability.total_checkins += 1
    user_ability.current_value = min(user_ability.current_value + 5, 100)
    user_ability.last_checkin_date = today

    exp_result = ExpService.add_exp(user_id, exp)

    db.session.commit()

    new_achievements = AchievementService.check_achievements(user_id)

    return jsonify({
        'success': True,
        'exp_gained': exp,
        'total_exp': exp_result['total_exp'],
        'level': exp_result['new_level'],
        'level_up': exp_result['level_up'],
        'new_achievements': [{'name': a.name, 'icon': a.icon} for a in new_achievements]
    })

@bp.route('/history', methods=['GET'])
def get_history():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    checkins = Checkin.query.filter_by(user_id=user_id).order_by(
        Checkin.checkin_date.desc()
    ).paginate(page=page, per_page=per_page)

    items = []
    for c in checkins.items:
        items.append({
            'id': c.id,
            'ability_name': c.ability.name,
            'ability_icon': c.ability.icon,
            'ability_color': c.ability.color,
            'date': c.checkin_date.isoformat(),
            'exp_gained': c.exp_gained,
            'note': c.note,
            'mood': c.mood
        })

    return jsonify({
        'items': items,
        'total': checkins.total,
        'pages': checkins.pages,
        'current_page': page
    })

@bp.route('/calendar', methods=['GET'])
def get_calendar():
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

    checkins = Checkin.query.filter(
        Checkin.user_id == user_id,
        Checkin.checkin_date >= start_date,
        Checkin.checkin_date <= end_date
    ).all()

    calendar_data = {}
    daily_exp = {}
    for c in checkins:
        date_str = c.checkin_date.isoformat()
        if date_str not in calendar_data:
            calendar_data[date_str] = []
            daily_exp[date_str] = 0
        calendar_data[date_str].append({
            'ability_name': c.ability.name,
            'ability_icon': c.ability.icon
        })
        daily_exp[date_str] += c.exp_gained

    return jsonify({
        'year': year,
        'month': month,
        'calendar_data': calendar_data,
        'daily_exp': daily_exp
    })
