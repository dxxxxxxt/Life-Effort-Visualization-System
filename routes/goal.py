from flask import Blueprint, request, jsonify, session
from models import db
from models.goal import Goal
from datetime import datetime, date

bp = Blueprint('goal', __name__, url_prefix='/api/goals')

@bp.route('', methods=['GET'])
def get_goals():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    status = request.args.get('status')

    query = Goal.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)

    goals = query.order_by(Goal.created_at.desc()).all()

    return jsonify({
        'goals': [{
            'id': g.id,
            'title': g.title,
            'description': g.description,
            'ability_id': g.ability_id,
            'ability_name': g.ability.name if g.ability else None,
            'target_value': g.target_value,
            'current_value': g.current_value,
            'progress': int(g.current_value / g.target_value * 100) if g.target_value else 0,
            'start_date': g.start_date.isoformat() if g.start_date else None,
            'end_date': g.end_date.isoformat() if g.end_date else None,
            'status': g.status
        } for g in goals]
    })

@bp.route('', methods=['POST'])
def create_goal():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    data = request.get_json()
    goal = Goal(
        user_id=user_id,
        ability_id=data.get('ability_id'),
        title=data.get('title'),
        description=data.get('description', ''),
        target_value=data.get('target_value', 0),
        current_value=0,
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else date.today(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
        status='active'
    )
    db.session.add(goal)
    db.session.commit()

    return jsonify({
        'success': True,
        'goal': {
            'id': goal.id,
            'title': goal.title,
            'target_value': goal.target_value
        }
    })

@bp.route('/<int:goal_id>', methods=['PUT'])
def update_goal(goal_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
    if not goal:
        return jsonify({'error': '目标不存在'}), 404

    data = request.get_json()
    goal.title = data.get('title', goal.title)
    goal.description = data.get('description', goal.description)
    goal.target_value = data.get('target_value', goal.target_value)
    goal.current_value = data.get('current_value', goal.current_value)
    goal.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else goal.end_date

    if goal.target_value and goal.current_value >= goal.target_value:
        goal.status = 'completed'

    db.session.commit()

    return jsonify({'success': True})

@bp.route('/<int:goal_id>/complete', methods=['PUT'])
def complete_goal(goal_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
    if not goal:
        return jsonify({'error': '目标不存在'}), 404

    goal.status = 'completed'
    goal.current_value = goal.target_value
    db.session.commit()

    return jsonify({'success': True})

@bp.route('/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
    if not goal:
        return jsonify({'error': '目标不存在'}), 404

    db.session.delete(goal)
    db.session.commit()

    return jsonify({'success': True})
