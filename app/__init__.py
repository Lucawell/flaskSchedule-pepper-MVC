from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_admin import Admin
from flask_mail import Mail
from flask_uploads import configure_uploads
import logging
from logging.handlers import RotatingFileHandler
from flask_apscheduler import APScheduler


# 创建Flask应用实例
db = SQLAlchemy()  # 数据库实例
login_manager = LoginManager()  # 登录管理实例
migrate = Migrate()  # 数据库迁移实例
mail = Mail()  # 邮件实例
scheduler = APScheduler()


def create_app() -> Flask:
    """创建Flask应用实例并进行初始化设置。

    Returns:
        Flask: 初始化设置后的Flask应用实例。
    """
    app = Flask(__name__)
    app.config.from_object('app.config')
    app.config.from_envvar('FLASKR_CONFIGS')

    configure_logging(app)  # 添加日志配置
    initialize_extensions(app)  # 初始化
    register_blueprints(app)  # 注册蓝图
    configure_api_resources(app)  # 配置api
    configure_admin(app)  # 配置管理员
    # configure_scheduler(app)

    return app

def initialize_extensions(app: Flask) -> None:
    """初始化扩展，包括数据库、登录管理、数据库迁移、邮件和文件上传。

    Args:
        app (Flask): Flask应用实例。
    """
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    mail.init_app(app)

    from app.controller.api_controller import photos
    configure_uploads(app, photos)


def register_blueprints(app: Flask) -> None:
    """注册蓝图，包括主页、用户、事件和提醒蓝图。

    Args:
        app (Flask): Flask应用实例。
    """
    from app.views.index_view import index_blueprint
    from app.views.user_view import user_blueprint
    from app.views.event_view import event_blueprint
    from app.views.reminder_view import reminder_blueprint
    from app.views.album_view import album_blueprint

    app.register_blueprint(index_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(event_blueprint, url_prefix='/event')
    app.register_blueprint(reminder_blueprint, url_prefix='/reminder')
    app.register_blueprint(album_blueprint, url_prefix='/album')


def configure_api_resources(app: Flask) -> None:
    """配置API资源，包括事件、消息、邮件、短信和文件上传资源。

    Args:
        app (Flask): Flask应用实例。
    """
    api = Api(app)

    from app.controller.api_controller import (
        EventResource, MessageResource, EmailResource, SMSResource, FileUploadResource
    )

    api.add_resource(EventResource, '/api/events/<int:user_id>')
    api.add_resource(MessageResource, '/api/receive-message')
    api.add_resource(EmailResource, '/api/send-email')
    api.add_resource(SMSResource, '/api/send-sms')
    api.add_resource(FileUploadResource, '/api/upload')


def configure_admin(app: Flask) -> None:
    """配置Flask-Admin管理界面，包括自定义首页和用户、事件管理视图。

    Args:
        app (Flask): Flask应用实例。
    """
    from app.views.admin_view import MyAdminIndexView, UserAdminView, EventAdminView, EmailHistoryAdminView
    from app.model.User import User
    from app.model.Event import Event
    from app.model.EmailHistory import EmailHistory

    admin = Admin(app, index_view=MyAdminIndexView())
    admin.add_view(UserAdminView(User, db.session, url='users', name='users', endpoint='users_admin'))
    admin.add_view(EventAdminView(Event, db.session, url='events', name='events', endpoint='events_admin'))
    admin.add_view(EmailHistoryAdminView(EmailHistory, db.session, url='email-history', name='email-history',
                                         endpoint='email_history_admin'))


def configure_logging(app: Flask) -> None:
    """配置应用程序日志。

    Args:
        app (Flask): Flask应用实例。
    """
    log_file_path = 'app.log'
    log_handler = RotatingFileHandler(log_file_path, maxBytes=10240, backupCount=10)
    log_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    log_handler.setLevel(logging.INFO)
    app.logger.addHandler(log_handler)


def configure_scheduler(app: Flask) -> None:
    """配置定时任务。

    Args:
        app (Flask): Flask应用实例。
    """
    from app.controller.reminder_controller import check_reminder
    scheduler.init_app(app)
    scheduler.add_job(id='reminder_job', func=check_reminder, args=[1], trigger='interval', seconds=5)
    scheduler.start()





