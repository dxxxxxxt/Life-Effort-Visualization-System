from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User, LevelConfig
from models.ability import Ability, UserAbility
from models.checkin import Checkin
from models.achievement import Achievement, UserAchievement
from models.note import Note
from models.goal import Goal
