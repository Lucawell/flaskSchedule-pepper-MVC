from app.model.User import User
from app.model.Event import Event

from app import app, db
from flask import request, render_template, jsonify, url_for, redirect


@app.route("/")
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    new_user = User(name=name, email=email, phone=phone)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('index'))

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_user.html', user=user)


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/events')
def event_list():
    events = Event.query.all()
    return render_template('events.html', events=events)

@app.route('/add_event', methods=['POST'])
def add_event():
    user_id = request.form['user_id']
    title = request.form['title']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    location = request.form['location']
    description = request.form['description']

    new_event = Event(user_id=user_id, title=title, start_time=start_time, end_time=end_time, location=location, description=description)
    db.session.add(new_event)
    db.session.commit()

    return redirect(url_for('event_list'))

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return redirect(url_for('event_list'))

    if request.method == 'POST':
        event.user_id = request.form['user_id']
        event.title = request.form['title']
        event.start_time = request.form['start_time']
        event.end_time = request.form['end_time']
        event.location = request.form['location']
        event.description = request.form['description']
        db.session.commit()
        return redirect(url_for('event_list'))

    return render_template('events.html', event=event)

@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()

    return redirect(url_for('event_list'))

# 发送消息
@app.route("/getdata")
def getdata():
    # 查询所有用户记录
    users = User.query.all()
    # 创建一个 JSON 对象
    json_data = []
    for user in users:
        # 将用户记录添加到 JSON 对象
        json_data.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone
        })
    # 使用 jsonify() 函数来序列化 JSON 对象
    json_response = jsonify(json_data)

    # 使用 return 语句返回 JSON 对象
    return json_response

# 接收消息
@app.route('/receive_message', methods=['POST', 'GET'])
def receive_message():
    if request.method == 'POST':
        data = request.form.get('message')
        print("Received message:", data)
        if data:
            return data  # 返回消息文本
        else:
            return "No message received."
    else:
        return "GET request received."
