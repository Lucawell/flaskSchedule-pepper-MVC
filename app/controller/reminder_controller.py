from datetime import datetime, timedelta
from flask import request, render_template, redirect, url_for, current_app, session
from flask_login import login_required, current_user
from flask_mail import Message

from app import db, scheduler
from app.model.EmailHistory import EmailHistory
from app.model.User import User
from app.model.Event import Event


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
    到用户的电子邮件地址。保存已发送的电子邮件到历史记录。

    Returns:
        带有表单数据的呈现的“email_history.html”模板。
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
        # 将已发送的电子邮件保存到历史记录
        email_history = EmailHistory(user_id=current_user.id, title=title, content=content,
                                     recipients=", ".join(recipients))
        db.session.add(email_history)
        db.session.commit()
    return redirect(url_for('reminder.show_email_history'))
    # return show_email_history()
    # return render_template('email_history.html', form=request.form)


# 显示历史记录
@login_required
def show_email_history():
    """
    显示当前用户的电子邮件历史记录。
    此函数从数据库中检索当前用户的电子邮件历史记录，并将其呈现到“email_history.html”模板中。
    Returns:
        带有电子邮件历史记录的“email_history.html”模板。
    """
    email_history = EmailHistory.query.filter_by(user_id=current_user.id).all()
    return render_template('email_history.html', email_history=email_history)


# 删除历史记录
@login_required
def delete_email_history(email_history_id):
    """
    从数据库中删除指定的电子邮件历史记录。
    此函数从数据库中删除指定的电子邮件历史记录.
    Args:
        email_history_id (int): 要删除的电子邮件历史记录的 ID。
    Returns:
        带有电子邮件历史记录的“email_history.html”模板。
    """
    email_history = EmailHistory.query.filter_by(id=email_history_id).first()
    if email_history and email_history.user_id == current_user.id:
        db.session.delete(email_history)
        db.session.commit()
    return show_email_history()


# 浏览器提醒
# 定义定时任务
def check_reminder(user_id):
    with scheduler.app.app_context():
        # 获取当前时间
        current_time = datetime.now().time()
        # 获取用户id

        # 查询需要提醒的事件，仅限当前用户
        events_to_remind = Event.query.filter(
            Event.user_id == user_id,
            Event.event_time <= current_time,
            Event.reminder_type != "none",
        ).all()

        for event in events_to_remind:
            # 计算提醒时间
            reminder_time = timedelta(minutes=event.reminder_time)
            reminder_datetime = datetime.combine(event.start_date, event.event_time) - reminder_time

            # 检查是否到达提醒时间
            if current_time >= reminder_datetime.time():
                # 在这里执行提醒逻辑，可以使用 Flask-SocketIO 或其他方式通知前端
                print(f"Reminder for event '{event.title}' at {current_time}")


