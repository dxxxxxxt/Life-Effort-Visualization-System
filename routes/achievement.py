from flask import Blueprint, jsonify, session
from models.achievement import Achievement, UserAchievement
from services.achievement_service import AchievementService

bp = Blueprint('achievement', __name__, url_prefix='/api/achievements')

@bp.route('', methods=['GET'])
def get_achievements():
    achievements = Achievement.query.all()
    return jsonify({
        'achievements': [{
            'id': a.id,
            'name': a.name,
            'description': a.description,
            'icon': a.icon,
            'type': a.achievement_type,
            'requirement': a.requirement_value,
            'exp_reward': a.exp_reward
        } for a in achievements]
    })

@bp.route('/user', methods=['GET'])
def get_user_achievements():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    result = AchievementService.get_user_achievements(user_id)
    return jsonify(result)

@bp.route('/progress', methods=['GET'])
def get_achievement_progress():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    from models.checkin import Checkin
    from services.exp_service import ExpService
    from models.user import User

    total_checkins = Checkin.query.filter_by(user_id=user_id).count()
    streak = ExpService.get_current_streak(user_id)
    max_streak = AchievementService.get_max_streak(user_id)

    user = User.query.get(user_id)

    return jsonify({
        'total_checkins': total_checkins,
        'current_streak': streak,
        'max_streak': max_streak,
        'level': user.level
    })
