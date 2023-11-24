# encoding:utf-8
from datetime import timedelta, datetime
from app.model.Event import Event
from app import db
from flask import request, render_template, url_for, redirect, flash
from app.forms import EventForm
from flask_login import login_required, current_user


@login_required
def show_event():
    # 查询当前用户的所有事件
    events = Event.query.filter_by(user_id=current_user.id).all()
    today = datetime.now().date()  # 获取当前日期
    today_events = []
    expired_events = []
    for event in events:
        # 如果事件过期，将其添加到过期事件列表中
        if event.end_date < today:
            expired_events.append(event)
            continue
        # 如果事件不是重复事件，将其添加到今天事件列表中
        if event.repeat == "none" and today <= event.end_date:
            today_events.append(event)
        # 如果事件是重复事件，动态生成后将其添加到今天事件列表中
        else:
            start_date = event.start_date
            end_date = event.end_date

            if event.repeat == "daily":
                current_date = start_date
                while current_date <= end_date:
                    if current_date >= today:
                        new_event = generate_repeat_event(event, current_date)
                        today_events.append(new_event)
                        break
                    current_date += timedelta(days=1)
            elif event.repeat == "weekly":
                if end_date-today < timedelta(days=7):
                    expired_events.append(event)
                    continue
                current_date = start_date
                while current_date <= end_date:
                    if current_date >= today:
                        last_week_event = generate_repeat_event(event, current_date)
                        today_events.append(last_week_event)
                        break
                    current_date += timedelta(weeks=1)
            elif event.repeat == "monthly":
                if end_date-today < timedelta(days=30):
                    expired_events.append(event)
                    continue
                current_date = start_date
                while current_date <= end_date:
                    if current_date >= today:
                        last_month_event = generate_repeat_event(event, current_date)
                        today_events.append(last_month_event)
                        break
                    current_date += timedelta(days=30)
    return render_template('event_list.html', events=today_events, expired_events=expired_events)
# 创建一个函数，用于生成重复事件
@login_required
def generate_repeat_event(event, current_date):
    new_event = Event(
        user_id=event.user_id,
        title=event.title,
        start_date=current_date,
        end_date=current_date,
        event_time=event.event_time,
        location=event.location,
        description=event.description,
        repeat=event.repeat,
        reminder_type=event.reminder_type,
        reminder_time=event.reminder_time
    )
    new_event.id = event.id  # 设置新事件的ID为原事件的ID
    return new_event

@login_required
def calendar():
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('calendar.html', events=events)

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
        event_time = form.event_time.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        location = form.location.data
        description = form.description.data
        repeat = form.repeat.data  # 从表单获取重复类型
        reminder_type = form.reminder_type.data
        reminder_time = form.reminder_time.data

        # 创建事件对象并保存到数据库
        event = Event(
            user_id=current_user.id,  # 使用当前登录用户的 ID
            title=title,
            event_time=event_time,
            start_date=start_date,
            end_date=end_date,
            location=location,
            description=description,
            repeat=repeat,  # 设置事件的重复类型
            reminder_type=reminder_type,
            reminder_time=reminder_time
        )
        db.session.add(event)
        db.session.commit()

        flash('事件创建成功', 'success')

        return redirect(url_for('event.show_event'))  # 重定向到事件列表页面或其他适当的页面

    return render_template('create_event.html', form=form)


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

    return redirect(url_for('event.show_event'))


@login_required
def edit_event(event_id):
    # 查询要编辑的事件
    event = Event.query.get(event_id)

    # 检查事件是否存在并属于当前用户
    if not event or event.user_id != current_user.id:
        flash('无法编辑事件', 'error')
        return redirect(url_for('event.show_event'))

    form = EventForm(obj=event)  # 使用事件对象填充表单

    if form.validate_on_submit():
        # 更新事件信息
        event.title = form.title.data
        event.event_time = form.event_time.data
        event.start_date = form.start_date.data
        event.end_date = form.end_date.data
        event.location = form.location.data
        event.description = form.description.data
        event.repeat = form.repeat.data  # 从表单获取重复类型
        event.reminder_type = form.reminder_type.data
        event.reminder_time = form.reminder_time.data

        db.session.commit()
        flash('事件更新成功', 'success')
        return redirect(url_for('event.show_event'))

    return render_template('edit_event.html', form=form)
