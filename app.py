from flask import Flask, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, current_user
import os
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    from models import db
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'index'

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import bp as auth_bp
    from routes.checkin import bp as checkin_bp
    from routes.abilities import bp as abilities_bp
    from routes.stats import bp as stats_bp
    from routes.achievement import bp as achievement_bp
    from routes.note import bp as note_bp
    from routes.goal import bp as goal_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(checkin_bp)
    app.register_blueprint(abilities_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(achievement_bp)
    app.register_blueprint(note_bp)
    app.register_blueprint(goal_bp)

    @app.route('/')
    def index():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return render_template('dashboard.html')

    @app.route('/stats')
    def stats_page():
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return render_template('stats.html')

    @app.route('/achievements')
    def achievements_page():
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return render_template('achievements.html')

    @app.route('/notes')
    def notes_page():
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return render_template('notes.html')

    @app.route('/goals')
    def goals_page():
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return render_template('goals.html')

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from models import db
        db.create_all()
        from init_db import init_data
        init_data()
    app.run(debug=True, host='0.0.0.0', port=5000)
