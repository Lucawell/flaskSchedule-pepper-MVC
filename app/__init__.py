# # encoding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    app.config.from_envvar('FLASKR_CONFIGS')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'  # 设置登录视图的名称（在这个示例中是 'user.login'）

    from app.views.index_view import index_blueprint
    from app.views.user_view import user_blueprint
    from app.views.event_view import event_blueprint
    from app.views.reminder_view import reminders_blueprint

    from app.controller.api_controller import api_login_blueprint

    app.register_blueprint(index_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(event_blueprint, url_prefix='/event')
    app.register_blueprint(reminders_blueprint, url_prefix='/reminders')
    app.register_blueprint(api_login_blueprint)

    return app
