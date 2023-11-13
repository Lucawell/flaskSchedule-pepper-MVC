# encoding:utf-8
from flask_mail import Mail, Message
from app import create_app, mail  # 假设你的 Flask 应用工厂函数是 create_app

def send_email(subject, recipients, html):
    app = create_app()
    with app.app_context():
        msg = Message(subject, recipients=recipients, html=html)
        # msg.html = "<b>testing, html</b>"
        mail.send(msg)

if __name__ == '__main__':
    send_email('测试邮件', ['2857394761@qq.com'], '<b>测试Flask发送邮件<b>')

