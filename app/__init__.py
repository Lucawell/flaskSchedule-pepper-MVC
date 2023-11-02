# # encoding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    app.config.from_envvar('FLASKR_CONFIGS')
    # 初始化数据库
    db.init_app(app)
    # 注册migrate，创建数据库迁移
    migrate.init_app(app, db)
    # 登录管理
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'  # 设置登录视图的名称（在这个示例中是 'user.login'）

    # 初始化JWTManager
    jwt = JWTManager(app)
    api = Api(app)

    # 导入数据库模型
    from app.model.Admin import Admin
    from app.model.User import User
    from app.model.Event import Event
    from app.model.Reminder import Reminder

    # 导入视图
    from app.views.index_view import index_blueprint
    from app.views.user_view import user_blueprint
    from app.views.event_view import event_blueprint
    from app.views.reminder_view import reminders_blueprint

    from app.controller.api_controller import EventListResource

    # 注册蓝图
    app.register_blueprint(index_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(event_blueprint, url_prefix='/event')
    app.register_blueprint(reminders_blueprint, url_prefix='/reminders')

    # 将资源添加到您的 API
    api.add_resource(EventListResource, '/api/events')

    return app
