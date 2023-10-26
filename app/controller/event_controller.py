# encoding:utf-8
from app.model.Event import Event
from app import app, db
from flask import request, render_template, url_for, redirect

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