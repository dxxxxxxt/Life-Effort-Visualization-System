from models import db
from models.checkin import Checkin
from models.ability import UserAbility
from models.achievement import Achievement, UserAchievement
from models.user import User
from sqlalchemy import func, distinct
from services.exp_service import ExpService
from datetime import date, timedelta

class AchievementService:

    @staticmethod
    def check_achievements(user_id):
        new_achievements = []
        achievements = Achievement.query.all()

        earned_ids = set(
            ua.achievement_id for ua in UserAchievement.query.filter_by(user_id=user_id).all()
        )

        for achievement in achievements:
            if achievement.id in earned_ids:
                continue

            earned = False

            if achievement.achievement_type == 'checkin':
                count = Checkin.query.filter_by(user_id=user_id).count()
                earned = count >= achievement.requirement_value

            elif achievement.achievement_type == 'streak':
                max_streak = AchievementService.get_max_streak(user_id)
                earned = max_streak >= achievement.requirement_value

            elif achievement.achievement_type == 'level':
                user = User.query.get(user_id)
                earned = user.level >= achievement.requirement_value

            elif achievement.achievement_type == 'special':
                if achievement.requirement_value == 7:
                    abilities_checked = db.session.query(
                        func.count(distinct(Checkin.ability_id))
                    ).filter_by(user_id=user_id).scalar()
                    earned = abilities_checked >= 7

            elif achievement.achievement_type == 'ability_checkin':
                if achievement.ability_id:
                    count = Checkin.query.filter_by(
                        user_id=user_id,
                        ability_id=achievement.ability_id
                    ).count()
                    earned = count >= achievement.requirement_value

            elif achievement.achievement_type == 'total_checkin':
                count = Checkin.query.filter_by(user_id=user_id).count()
                earned = count >= achievement.requirement_value

            if earned:
                user_achievement = UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement.id
                )
                db.session.add(user_achievement)
                ExpService.add_exp(user_id, achievement.exp_reward)
                new_achievements.append(achievement)

        if new_achievements:
            db.session.commit()

        return new_achievements

    @staticmethod
    def get_max_streak(user_id):
        dates = db.session.query(Checkin.checkin_date).filter_by(
            user_id=user_id
        ).distinct().order_by(Checkin.checkin_date.desc()).all()

        dates = [d[0] for d in dates]

        if not dates:
            return 0

        max_streak = 1
        current_streak = 1

        for i in range(1, len(dates)):
            prev_date = dates[i - 1]
            curr_date = dates[i]

            if (prev_date - curr_date).days == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1

        return max_streak

    @staticmethod
    def get_user_achievements(user_id):
        earned = UserAchievement.query.filter_by(user_id=user_id).order_by(UserAchievement.earned_at.desc()).all()
        all_achievements = Achievement.query.all()
        earned_ids = set(ea.achievement_id for ea in earned)

        result = {
            'earned': [],
            'locked': [],
            'total': len(all_achievements),
            'earned_count': len(earned)
        }

        for ea in earned:
            result['earned'].append({
                'id': ea.achievement.id,
                'name': ea.achievement.name,
                'description': ea.achievement.description,
                'icon': ea.achievement.icon,
                'earned_at': ea.earned_at.strftime('%Y-%m-%d')
            })

        for a in all_achievements:
            if a.id not in earned_ids:
                result['locked'].append({
                    'id': a.id,
                    'name': a.name,
                    'description': a.description,
                    'icon': a.icon,
                    'type': a.achievement_type,
                    'requirement': a.requirement_value
                })

        return result
