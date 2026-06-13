from flask import Blueprint, request, jsonify, session, current_app
from models import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import base64

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/register', methods=['POST'])
def register():
    # 支持 FormData 和 JSON 两种格式
    if request.content_type and 'multipart/form-data' in request.content_type:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        nickname = request.form.get('nickname', username)
        avatar_file = request.files.get('avatar')
    else:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        nickname = data.get('nickname', username)
        avatar_file = None

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400

    if len(username) < 3:
        return jsonify({'error': '用户名至少3个字符'}), 400

    if len(password) < 6:
        return jsonify({'error': '密码至少6个字符'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 400

    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        nickname=nickname
    )

    # 处理头像上传
    if avatar_file and allowed_file(avatar_file.filename):
        upload_folder = os.path.join(current_app.static_folder, 'img', 'avatars')
        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(f"{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
        filepath = os.path.join(upload_folder, filename)
        avatar_file.save(filepath)
        user.avatar = f"/static/img/avatars/{filename}"

    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id
    session['username'] = user.username

    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'level': user.level,
            'total_exp': user.total_exp,
            'avatar': user.avatar
        }
    })

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': '用户名或密码错误'}), 401

    user.last_login = datetime.utcnow()
    db.session.commit()

    session['user_id'] = user.id
    session['username'] = user.username

    progress, exp_needed, current_exp = user.get_exp_progress()

    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'level': user.level,
            'total_exp': user.total_exp,
            'level_title': user.get_level_title(),
            'avatar': user.avatar
        }
    })

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@bp.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    progress, exp_needed, current_exp = user.get_exp_progress()

    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'level': user.level,
            'level_title': user.get_level_title(),
            'total_exp': user.total_exp,
            'current_exp': current_exp,
            'next_level_exp': exp_needed,
            'exp_progress': progress,
            'avatar': user.avatar
        }
    })

@bp.route('/avatar', methods=['POST'])
def upload_avatar():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '未登录'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    avatar_file = request.files.get('avatar')
    if not avatar_file or not allowed_file(avatar_file.filename):
        return jsonify({'error': '请上传有效的图片文件'}), 400

    upload_folder = os.path.join(current_app.static_folder, 'img', 'avatars')
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(f"{user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
    filepath = os.path.join(upload_folder, filename)
    avatar_file.save(filepath)

    user.avatar = f"/static/img/avatars/{filename}"
    db.session.commit()

    return jsonify({
        'success': True,
        'avatar': user.avatar
    })
