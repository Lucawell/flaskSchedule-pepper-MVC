# encoding:utf-8
from app.model.Event import Event
from app import app, db
from flask import request, render_template, url_for, redirect, flash
from app.forms import EventForm
from flask_login import login_required, current_user

# ----------------------------------以下是测试部分，不要在生产环境调用-----------------------------------
# @app.route('/events')
# def event_list():
#     events = Event.query.all()
#     return render_template('events.html', events=events)

# @app.route('/add_event', methods=['POST'])
# def add_event():
#     user_id = request.form['user_id']
#     title = request.form['title']
#     start_time = request.form['start_time']
#     end_time = request.form['end_time']
#     location = request.form['location']
#     description = request.form['description']
#
#     new_event = Event(user_id=user_id,
#                       title=title,
#                       start_time=start_time,
#                       end_time=end_time,
#                       location=location,
#                       description=description)
#     db.session.add(new_event)
#     db.session.commit()
#
#     return redirect(url_for('event_list'))

# @app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
# def edit_event(event_id):
#     event = Event.query.get(event_id)
#     if not event:
#         return redirect(url_for('event_list'))
#
#     if request.method == 'POST':
#         event.user_id = request.form['user_id']
#         event.title = request.form['title']
#         event.start_time = request.form['start_time']
#         event.end_time = request.form['end_time']
#         event.location = request.form['location']
#         event.description = request.form['description']
#         db.session.commit()
#         return redirect(url_for('event_list'))
#
#     return render_template('events.html', event=event)

# @app.route('/delete_event/<int:event_id>')
# def delete_event(event_id):
#     event = Event.query.get(event_id)
#     if event:
#         db.session.delete(event)
#         db.session.commit()
#
#     return redirect(url_for('event_list'))

# ----------------------------------以下是生产和开发部分-----------------------------------

@app.route('/event_list')
@login_required
def event_list():
    # 查询当前用户的所有事件
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('event_list.html', events=events)
@app.route('/create_event', methods=['GET', 'POST'])
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
        return redirect(url_for('event_list'))  # 重定向到事件列表页面或其他适当的页面

    return render_template('create_event.html', form=form)


@app.route('/delete_event/<int:event_id>', methods=['POST'])
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

    return redirect(url_for('event_list'))

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    # 查询要编辑的事件
    event = Event.query.get(event_id)

    # 检查事件是否存在并属于当前用户
    if not event or event.user_id != current_user.id:
        flash('无法编辑事件', 'error')
        return redirect(url_for('event_list'))

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
        return redirect(url_for('event_list'))

    return render_template('edit_event.html', form=form)
