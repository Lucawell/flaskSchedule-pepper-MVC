# encoding:utf-8
from datetime import timedelta
from app.model.Event import Event, RepeatType
from app import db
from flask import request, render_template, url_for, redirect, flash
from app.forms import EventForm
from flask_login import login_required, current_user


@login_required
def event_list():
    # 查询当前用户的所有事件
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('event_list.html', events=events)


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
        repeat = form.repeat.data  # 从表单获取重复类型

        # 创建事件对象并保存到数据库
        event = Event(
            user_id=current_user.id,  # 使用当前登录用户的 ID
            title=title,
            start_time=start_time,
            end_time=end_time,
            location=location,
            description=description,
            repeat=repeat  # 设置事件的重复类型
        )

        db.session.add(event)
        db.session.commit()

        flash('事件创建成功', 'success')

        # 如果事件具有重复规则，则创建重复事件
        if repeat != RepeatType.NONE:
            recurring_events = create_recurring_events(event)
            for recurring_event in recurring_events:
                db.session.add(recurring_event)
            db.session.commit()

        return redirect(url_for('event.event_list'))  # 重定向到事件列表页面或其他适当的页面

    return render_template('create_event.html', form=form)

def create_recurring_events(event):
    if event.repeat == RepeatType.NONE:
        return [event]

    events = []
    current_date = event.start_time
    while current_date <= event.end_time:
        new_event = Event(
            user_id=event.user_id,
            title=event.title,
            start_time=current_date,
            end_time=current_date + event.duration,
            location=event.location,
            description=event.description,
            repeat=RepeatType.NONE
        )
        events.append(new_event)

        if event.repeat == RepeatType.DAILY:
            current_date += timedelta(days=1)
        elif event.repeat == RepeatType.WEEKLY:
            current_date += timedelta(weeks=1)
        elif event.repeat == RepeatType.MONTHLY:
            # Note: This is a simplified monthly repeat. You may need to handle month-specific date changes.
            current_date += timedelta(days=30)  # Adjust as needed

    return events


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
