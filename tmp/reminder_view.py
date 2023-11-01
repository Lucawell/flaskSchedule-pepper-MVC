# encoding:utf-8
from flask_login import login_required
from app.forms import ReminderForm
from app.model.Event import Event
from app.model.Reminder import Reminder
from app import db
from flask import Blueprint, request, render_template, url_for, redirect, flash

reminders_blueprint = Blueprint('reminders', __name__)

@reminders_blueprint.route('/reminders', methods=['GET'])
@login_required
def reminder_list():
    reminders = Reminder.query.all()  # 查询所有提醒
    return render_template('event_list.html', reminders=reminders)

@reminders_blueprint.route('/create_reminder/<int:event_id>', methods=['GET', 'POST'])
@login_required
def create_reminder(event_id):
    form = ReminderForm()  # 使用提醒表单来接收用户输入
    event = Event.query.get(event_id)  # 获取与提醒相关的事件

    if not event:
        flash('事件不存在或无权限创建提醒', 'error')
        return redirect(url_for('event.event_list'))

    if not form.validate_on_submit():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"字段 {field} 中的错误: {error}", 'error')

    if form.validate_on_submit():
        # 获取用户输入的提醒信息
        time = form.time.data
        method = form.method.data

        # 创建提醒对象并保存到数据库
        reminder = Reminder(
            event_id=event.id,
            time=time,
            method=method
        )

        db.session.add(reminder)
        db.session.commit()

        flash('提醒创建成功', 'success')
        return redirect(url_for('event.event_list'))  # 重定向到事件列表页面或其他适当的页面

    return render_template('create_reminder.html', form=form, event=event)

@reminders_blueprint.route('/delete_reminder/<int:reminder_id>', methods=['POST'])
@login_required
def delete_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)

    if not reminder:
        flash('提醒不存在或无权限删除', 'error')
        return redirect(url_for('event.event_list'))

    # 可以添加权限检查，确保只有提醒的创建者能删除

    db.session.delete(reminder)
    db.session.commit()

    flash('提醒删除成功', 'success')
    return redirect(url_for('event.event_list'))
