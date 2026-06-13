from models import db
from datetime import datetime, date

class Checkin(db.Model):
    __tablename__ = 'checkins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ability_id = db.Column(db.Integer, db.ForeignKey('abilities.id'), nullable=False)
    checkin_date = db.Column(db.Date, nullable=False)
    exp_gained = db.Column(db.Integer, default=10)
    note = db.Column(db.Text)
    mood = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('checkins', lazy='dynamic'))
    ability = db.relationship('Ability', backref=db.backref('checkins', lazy='dynamic'))

    __table_args__ = (db.UniqueConstraint('user_id', 'ability_id', 'checkin_date'),)
