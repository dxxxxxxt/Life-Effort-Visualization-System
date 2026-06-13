from models import db
from datetime import datetime

class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    badge_image = db.Column(db.String(255))
    achievement_type = db.Column(db.String(50))
    requirement_value = db.Column(db.Integer)
    exp_reward = db.Column(db.Integer, default=50)
    ability_id = db.Column(db.Integer, db.ForeignKey('abilities.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('user_achievements', lazy='dynamic'))
    achievement = db.relationship('Achievement', backref=db.backref('user_achievements', lazy='dynamic'))

    __table_args__ = (db.UniqueConstraint('user_id', 'achievement_id'),)
