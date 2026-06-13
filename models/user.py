from models import db
from flask_login import UserMixin
from datetime import datetime

class LevelConfig(db.Model):
    __tablename__ = 'level_config'
    level = db.Column(db.Integer, primary_key=True)
    exp_required = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(50))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(100))
    avatar = db.Column(db.String(255))
    level = db.Column(db.Integer, default=1)
    total_exp = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def get_level_title(self):
        config = LevelConfig.query.filter_by(level=self.level).first()
        return config.title if config else '新手入门'

    def get_exp_progress(self):
        current_config = LevelConfig.query.filter_by(level=self.level).first()
        next_config = LevelConfig.query.filter_by(level=self.level + 1).first()
        if not next_config:
            return 100, 0, 0
        current_required = current_config.exp_required if current_config else 0
        exp_in_level = self.total_exp - current_required
        exp_needed = next_config.exp_required - current_required
        current_exp = exp_in_level
        return min(int(exp_in_level / exp_needed * 100), 100), exp_needed, current_exp
