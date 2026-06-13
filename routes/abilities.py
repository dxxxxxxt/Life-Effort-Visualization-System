from flask import Blueprint, jsonify, session
from models import db
from models.ability import Ability, UserAbility

bp = Blueprint('abilities', __name__, url_prefix='/api/abilities')

@bp.route('', methods=['GET'])
def get_abilities():
    abilities = Ability.query.order_by(Ability.sort_order).all()
    return jsonify({
        'abilities': [{
            'id': a.id,
            'name': a.name,
            'description': a.description,
            'icon': a.icon,
            'color': a.color
        } for a in abilities]
    })

@bp.route('/user', methods=['GET'])
def get_user_abilities():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    abilities = Ability.query.order_by(Ability.sort_order).all()

    user_abilities = {
        ua.ability_id: ua
        for ua in UserAbility.query.filter_by(user_id=user_id).all()
    }

    radar_data = []
    for ability in abilities:
        ua = user_abilities.get(ability.id)
        value = ua.current_value if ua else 0

        radar_data.append({
            'id': ability.id,
            'name': ability.name,
            'value': min(value, 100),
            'max': 100,
            'checkins': ua.total_checkins if ua else 0,
            'icon': ability.icon,
            'color': ability.color
        })

    return jsonify({
        'abilities': radar_data,
        'raw_values': [d['value'] for d in radar_data],
        'names': [d['name'] for d in radar_data]
    })

@bp.route('/<int:ability_id>/progress', methods=['GET'])
def get_ability_progress(ability_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    from models.checkin import Checkin
    from sqlalchemy import func
    from datetime import datetime, timedelta

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)

    daily_checkins = db.session.query(
        Checkin.checkin_date,
        func.count(Checkin.id).label('count')
    ).filter(
        Checkin.user_id == user_id,
        Checkin.ability_id == ability_id,
        Checkin.checkin_date >= start_date
    ).group_by(Checkin.checkin_date).all()

    return jsonify({
        'ability_id': ability_id,
        'daily_data': [
            {'date': d.isoformat(), 'count': c}
            for d, c in daily_checkins
        ]
    })
