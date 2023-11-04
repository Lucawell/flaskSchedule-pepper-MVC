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
