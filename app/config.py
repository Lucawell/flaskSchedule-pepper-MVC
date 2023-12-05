# encoding:utf-8
import os
from datetime import timedelta, datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 调试模式是否开启
DEBUG = True
# 是否追踪对象的修改。
SQLALCHEMY_TRACK_MODIFICATIONS = True
# 查询时显示原始SQL语句
SQLALCHEMY_ECHO = False
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
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEBUG = True

# 短信配置
ALIYUN_ACCESS_KEY_ID = os.getenv('ALIYUN_ACCESS_KEY_ID')
ALIYUN_ACCESS_KEY_SECRET = os.getenv('ALIYUN_ACCESS_KEY_SECRET')
ALIYUN_REGION_ID = 'cn-hangzhou'

# api配置
API_TOKEN = os.getenv('API_TOKEN')

# 上传文件配置
# 获取当前日期
current_date = datetime.now().strftime("%Y/%m/%d")
UPLOADED_PHOTOS_DEST = os.path.join(os.path.dirname(__file__), f'uploads/images/{current_date}')
UPLOADS_AUTOSERVE = True

# 调度器配置
SCHEDULER_API_ENABLED = True

