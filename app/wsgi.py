# encoding:utf-8
import sys

sys.path.append('D:/Projects_D/pepper_robot/flask-mvc-pepper-schedule')
from app import create_app

app = create_app()
if __name__ == "__main__":
    app.run()
