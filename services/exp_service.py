from datetime import date, timedelta
from models import db
from models.checkin import Checkin
from models.user import User, LevelConfig

class ExpService:
    BASE_EXP = 10

    STREAK_BONUS = {
        7: 1.2,
        14: 1.3,
        30: 1.5,
    }

    @staticmethod
    def calculate_exp(user_id, ability_id):
        base_exp = ExpService.BASE_EXP
        streak = ExpService.get_current_streak(user_id, ability_id)
        multiplier = 1.0
        for days, bonus in sorted(ExpService.STREAK_BONUS.items(), reverse=True):
            if streak >= days:
                multiplier = bonus
                break
        return int(base_exp * multiplier)

    @staticmethod
    def get_current_streak(user_id, ability_id=None):
        today = date.today()
        query = Checkin.query.filter_by(user_id=user_id)
        if ability_id:
            query = query.filter_by(ability_id=ability_id)

        dates = query.with_entities(Checkin.checkin_date).distinct().order_by(Checkin.checkin_date.desc()).all()
        dates = [d[0] for d in dates]

        if not dates:
            return 0

        streak = 0
        check_date = today

        for d in dates:
            if d == check_date or d == check_date - timedelta(days=1):
                streak += 1
                check_date = d - timedelta(days=1)
            else:
                break

        return streak

    @staticmethod
    def get_level_from_exp(exp):
        levels = LevelConfig.query.order_by(LevelConfig.level).all()
        current_level = 1
        next_exp = levels[1].exp_required if len(levels) > 1 else 1000

        for lc in levels:
            if exp >= lc.exp_required:
                current_level = lc.level
            else:
                next_exp = lc.exp_required
                break

        return current_level, next_exp

    @staticmethod
    def add_exp(user_id, exp):
        user = User.query.get(user_id)
        old_level = user.level
        user.total_exp += exp

        new_level, _ = ExpService.get_level_from_exp(user.total_exp)
        user.level = new_level

        db.session.commit()

        return {
            'total_exp': user.total_exp,
            'old_level': old_level,
            'new_level': new_level,
            'level_up': new_level > old_level
        }
