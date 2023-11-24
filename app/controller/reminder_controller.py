from flask import request, render_template
from flask_login import login_required, current_user
from flask_mail import Message
from app import mail
from app.model.User import User


# 邮件发送逻辑
def send_email(subject, html, recipients):
    msg = Message(subject, recipients=recipients, html=html)
    mail.send(msg)

# 发送邮件
@login_required
def send_reminder_email():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        # 通过用户id获取用户邮箱
        user = User.query.filter_by(id=current_user.id).first()
        recipients = [user.email]
        name = user.name
        # 渲染邮件内容
        html = render_template('email_template.html', name=name, title=title, content=content)

        # 发送邮件
        send_email(title, html, recipients)
    return render_template('send_email.html', form=request.form)

