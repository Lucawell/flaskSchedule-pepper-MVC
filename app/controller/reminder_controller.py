from flask import request, render_template
from flask_login import login_required, current_user
from flask_mail import Message
from app.model.User import User


# 邮件发送逻辑
def send_email(subject, html, recipients):
    """
    发送包含指定主题、HTML 内容和收件人的电子邮件。

    Parameters:
    subject (str): 电子邮件的主题。
    html (str): 电子邮件的 HTML 内容。
    recipients (list): 要将电子邮件发送到的电子邮件地址列表。

    Returns:
    None
    """
    from app import mail
    msg = Message(subject, recipients=recipients, html=html)
    mail.send(msg)

# 发送邮件
@login_required
def send_reminder_email():
    """
    向当前用户发送提醒电子邮件。

    此函数处理 POST 请求以发送提醒电子邮件。它从表单数据中检索标题和内容，
    根据用户的 ID 获取用户的电子邮件地址，使用提供的数据呈现电子邮件模板，然后发送电子邮件
    到用户的电子邮件地址。

    Returns:
        带有表单数据的呈现的“send_email.html”模板。
    """
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

