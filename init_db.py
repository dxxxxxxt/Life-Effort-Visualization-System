from models import db
from models.ability import Ability
from models.achievement import Achievement
from models.user import LevelConfig

def init_data():
    if Ability.query.count() == 0:
        abilities = [
            Ability(name='科研学习', description='学术研究与知识积累', icon='book', color='#4A90D9', sort_order=1),
            Ability(name='编程能力', description='代码开发与技术能力', icon='code', color='#50C878', sort_order=2),
            Ability(name='自媒体', description='内容创作与运营', icon='camera-video', color='#FF6B6B', sort_order=3),
            Ability(name='运动健身', description='身体健康与锻炼', icon='heart-pulse', color='#FFD93D', sort_order=4),
            Ability(name='表达能力', description='沟通与演讲技巧', icon='chat-dots', color='#9B59B6', sort_order=5),
            Ability(name='竞赛能力', description='比赛与竞技表现', icon='trophy', color='#E67E22', sort_order=6),
            Ability(name='化妆技术', description='形象管理与美学', icon='palette', color='#E91E63', sort_order=7),
        ]
        db.session.add_all(abilities)

    if Achievement.query.count() == 0:
        achievements = [
            Achievement(name='初出茅庐', description='完成第一次打卡', achievement_type='checkin', requirement_value=1, icon='star', exp_reward=20),
            Achievement(name='坚持一周', description='连续打卡7天', achievement_type='streak', requirement_value=7, icon='fire', exp_reward=50),
            Achievement(name='半月坚持', description='连续打卡14天', achievement_type='streak', requirement_value=14, icon='fire', exp_reward=100),
            Achievement(name='月度达人', description='连续打卡30天', achievement_type='streak', requirement_value=30, icon='award', exp_reward=200),
            Achievement(name='全能选手', description='所有能力都打过卡', achievement_type='special', requirement_value=7, icon='gem', exp_reward=150),
            Achievement(name='学霸养成', description='科研学习打卡50次', achievement_type='ability_checkin', requirement_value=50, icon='book', exp_reward=100, ability_id=1),
            Achievement(name='代码大师', description='编程能力打卡50次', achievement_type='ability_checkin', requirement_value=50, icon='code', exp_reward=100, ability_id=2),
            Achievement(name='健身达人', description='运动健身打卡30次', achievement_type='ability_checkin', requirement_value=30, icon='heart-pulse', exp_reward=80, ability_id=4),
            Achievement(name='勤奋新星', description='累计打卡100次', achievement_type='total_checkin', requirement_value=100, icon='rocket', exp_reward=200),
            Achievement(name='成长之路', description='达到5级', achievement_type='level', requirement_value=5, icon='bar-chart', exp_reward=100),
        ]
        db.session.add_all(achievements)

    if LevelConfig.query.count() == 0:
        levels = [
            LevelConfig(level=1, exp_required=0, title='新手入门'),
            LevelConfig(level=2, exp_required=100, title='初窥门径'),
            LevelConfig(level=3, exp_required=300, title='小有成就'),
            LevelConfig(level=4, exp_required=600, title='渐入佳境'),
            LevelConfig(level=5, exp_required=1000, title='驾轻就熟'),
            LevelConfig(level=6, exp_required=1500, title='炉火纯青'),
            LevelConfig(level=7, exp_required=2200, title='登峰造极'),
            LevelConfig(level=8, exp_required=3000, title='一代宗师'),
            LevelConfig(level=9, exp_required=4000, title='出神入化'),
            LevelConfig(level=10, exp_required=5500, title='超凡入圣'),
        ]
        db.session.add_all(levels)

    db.session.commit()
    print("Database initialized successfully!")
