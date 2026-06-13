from flask import Blueprint, request, jsonify, session
from models import db
from models.note import Note
from datetime import datetime, date

bp = Blueprint('note', __name__, url_prefix='/api/notes')

@bp.route('', methods=['GET'])
def get_notes():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    note_date = request.args.get('date')

    query = Note.query.filter_by(user_id=user_id)

    if note_date:
        query = query.filter_by(note_date=datetime.strptime(note_date, '%Y-%m-%d').date())

    notes = query.order_by(Note.note_date.desc()).paginate(page=page, per_page=per_page)

    return jsonify({
        'items': [{
            'id': n.id,
            'title': n.title,
            'content': n.content,
            'mood': n.mood,
            'date': n.note_date.isoformat(),
            'created_at': n.created_at.isoformat()
        } for n in notes.items],
        'total': notes.total,
        'pages': notes.pages,
        'current_page': page
    })

@bp.route('', methods=['POST'])
def create_note():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    data = request.get_json()
    title = data.get('title', '')
    content = data.get('content', '')
    mood = data.get('mood')
    note_date = data.get('date', date.today().isoformat())

    note = Note(
        user_id=user_id,
        title=title,
        content=content,
        mood=mood,
        note_date=datetime.strptime(note_date, '%Y-%m-%d').date() if isinstance(note_date, str) else note_date
    )
    db.session.add(note)
    db.session.commit()

    return jsonify({
        'success': True,
        'note': {
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'mood': note.mood,
            'date': note.note_date.isoformat()
        }
    })

@bp.route('/<int:note_id>', methods=['GET'])
def get_note(note_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({'error': '笔记不存在'}), 404

    return jsonify({
        'note': {
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'mood': note.mood,
            'date': note.note_date.isoformat(),
            'created_at': note.created_at.isoformat()
        }
    })

@bp.route('/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({'error': '笔记不存在'}), 404

    data = request.get_json()
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    note.mood = data.get('mood', note.mood)
    note.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        'success': True,
        'note': {
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'mood': note.mood
        }
    })

@bp.route('/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({'error': '笔记不存在'}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({'success': True})
