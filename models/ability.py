from models import db
from datetime import datetime

class Ability(db.Model):
    __tablename__ = 'abilities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    color = db.Column(db.String(20))
    sort_order = db.Column(db.Integer, default=0)

class UserAbility(db.Model):
    __tablename__ = 'user_abilities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ability_id = db.Column(db.Integer, db.ForeignKey('abilities.id'), nullable=False)
    current_value = db.Column(db.Integer, default=0)
    total_checkins = db.Column(db.Integer, default=0)
    last_checkin_date = db.Column(db.Date)

    user = db.relationship('User', backref=db.backref('user_abilities', lazy='dynamic'))
    ability = db.relationship('Ability', backref=db.backref('user_abilities', lazy='dynamic'))

    __table_args__ = (db.UniqueConstraint('user_id', 'ability_id'),)
