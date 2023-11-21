# # encoding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_admin import Admin
from flask_mail import Mail


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()


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
    # api管理
    api = Api(app)
    # 邮件管理
    mail.init_app(app)

    # 导入数据库模型
    from app.model.User import User
    from app.model.Event import Event

    # 导入视图
    from app.views.index_view import index_blueprint
    from app.views.user_view import user_blueprint
    from app.views.event_view import event_blueprint
    from app.views.reminder_view import reminder_blueprint
    from app.views.admin_view import MyAdminIndexView, UserAdminView, EventAdminView

    # 导入控制器
    from app.controller.api_controller import EventResource, MessageResource

    # 注册蓝图
    app.register_blueprint(index_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(event_blueprint, url_prefix='/event')
    app.register_blueprint(reminder_blueprint, url_prefix='/reminder')

    # 将资源添加到您的 API
    api.add_resource(EventResource, '/api/events/<int:user_id>')
    api.add_resource(MessageResource, '/api/receive-message')

    # 管理员
    admin = Admin(app, index_view=MyAdminIndexView())
    admin.add_view(UserAdminView(User, db.session, url='users', name='users', endpoint='users_admin'))
    admin.add_view(EventAdminView(Event, db.session, url='events', name='events', endpoint='events_admin'))

    return app
