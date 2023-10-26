# encoding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 创建项目对象
app = Flask(__name__)

app.config.from_object('app.setting')  # 模块下的setting文件名，不用加py后缀
app.config.from_envvar('FLASKR_SETTINGS')  # 环境变量，指向配置文件setting的路径

# 创建数据库对象
db = SQLAlchemy(app)

# app 導入後才能import
from app.model import User, Event, Reminder

# 只有在app对象之后声明，用于导入view模块
from app.controller import manage
