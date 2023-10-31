# encoding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required

# 创建项目对象
app = Flask(__name__)
app.config.from_object('app.config')  # 模块下的config文件名，不用加py后缀
app.config.from_envvar('FLASKR_CONFIGS')  # 环境变量，指向配置文件config的路径
# 创建数据库对象
db = SQLAlchemy(app)
# 登录配置
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'  # 设置登录视图的名称（在这个示例中是 'login'）

# app 導入後才能import
from app.model import User, Event, Reminder
# 只有在app对象之后声明，用于导入view模块
from app.controller import user_controller, event_controller, message_controller, reminder_controller



