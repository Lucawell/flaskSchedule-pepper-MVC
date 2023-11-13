# encoding:utf-8
from datetime import timedelta
# 调试模式是否开启
DEBUG = True
# 是否追踪对象的修改。
SQLALCHEMY_TRACK_MODIFICATIONS = True
# 查询时显示原始SQL语句
SQLALCHEMY_ECHO = True
# session必须要设置key
SECRET_KEY = 'c798ee1f5fd894f6e0ba9fc0d16b8b22'
# mysql数据库连接信息
DATABASE = 'schedule'
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost/" + DATABASE

# JWT令牌的过期时间
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

# 邮件配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = '1535744300@qq.com'
MAIL_DEFAULT_SENDER = '1535744300@qq.com'
MAIL_PASSWORD = 'fepnmbhhyyrjjdhg'
MAIL_DEBUG = True
