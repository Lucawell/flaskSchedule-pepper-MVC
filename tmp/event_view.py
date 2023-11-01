# encoding:utf-8
from app.model.Event import Event
from app.model.Reminder import Reminder
from app import db
from flask import Blueprint, request, render_template, url_for, redirect, flash
from app.forms import EventForm
from flask_login import login_required, current_user

event_blueprint = Blueprint('event', __name__)


@event_blueprint.route('/event_list')
@login_required
def event_list():
    # 查询当前用户的所有事件
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('event_list.html', events=events)


@event_blueprint.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()  # 使用您的事件表单来接收用户输入
    if not form.validate_on_submit():
        for field, errors in form.errors.items():
            for error in errors:
                print(f"字段 {field} 中的错误: {error}")
    if form.validate_on_submit():
        # 获取用户输入的事件信息
        title = form.title.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        location = form.location.data
        description = form.description.data

        # 创建事件对象并保存到数据库
        event = Event(
            user_id=current_user.id,  # 使用当前登录用户的 ID
            title=title,
            start_time=start_time,
            end_time=end_time,
            location=location,
            description=description
        )

        db.session.add(event)
        db.session.commit()

        flash('事件创建成功', 'success')
        return redirect(url_for('event.event_list'))  # 重定向到事件列表页面或其他适当的页面

    return render_template('create_event.html', form=form)


@event_blueprint.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    # 查询要删除的事件
    event = Event.query.get(event_id)

    # 检查事件是否存在并属于当前用户
    if event and event.user_id == current_user.id:
        db.session.delete(event)
        db.session.commit()
        flash('事件删除成功', 'success')
    else:
        flash('无法删除事件', 'error')

    return redirect(url_for('event.event_list'))


@event_blueprint.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    # 查询要编辑的事件
    event = Event.query.get(event_id)

    # 检查事件是否存在并属于当前用户
    if not event or event.user_id != current_user.id:
        flash('无法编辑事件', 'error')
        return redirect(url_for('event.event_list'))

    form = EventForm(obj=event)  # 使用事件对象填充表单

    if form.validate_on_submit():
        # 更新事件信息
        event.title = form.title.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.location = form.location.data
        event.description = form.description.data

        db.session.commit()
        flash('事件更新成功', 'success')
        return redirect(url_for('event.event_list'))

    return render_template('edit_event.html', form=form)
