# encoding:utf-8
import logging
import sys

sys.path.append('D:/Projects_D/pepper_robot/flask-mvc-pepper-schedule')
from app import create_app

# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为 INFO，你可以根据需要调整
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # 将日志写入文件
        logging.StreamHandler()  # 在控制台输出日志
    ]
)
app = create_app()
if __name__ == "__main__":
    app.run()
