from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # 添加密码哈希字段
    is_admin = db.Column(db.Boolean, default=False, nullable=False)  # 新增 is_admin 字段

    event = db.relationship('Event', backref='user', lazy='dynamic')
    email_history = db.relationship('EmailHistory', backref='user', lazy='dynamic')

    def __init__(self, name, email, phone, password, is_admin=False):
        self.name = name
        self.email = email
        self.phone = phone
        self.set_password(password)  # 在初始化时设置密码哈希值
        self.is_admin = is_admin  # 设置用户是否是管理员

    def __repr__(self):
        return '<User %r>' % self.name

    # 添加密码哈希相关的方法
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 实现 is_active 方法
    def is_active(self):
        return True  # 返回 True 表示用户是活动的，可以登录
