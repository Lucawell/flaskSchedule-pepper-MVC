# encoding:utf-8
from app.model.Reminder import Reminder
from app import app, db
from flask import request, render_template, url_for, redirect

@app.route('/reminders')
def reminder_list():
    reminders = Reminder.query.all()
    return render_template('reminders.html', reminders=reminders)

@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    event_id = request.form['event_id']
    time = request.form['time']
    method = request.form['method']

    new_reminder = Reminder(event_id=event_id, time=time, method=method)
    db.session.add(new_reminder)
    db.session.commit()

    return redirect(url_for('reminder_list'))

@app.route('/edit_reminder/<int:reminder_id>', methods=['GET', 'POST'])
def edit_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return redirect(url_for('reminder_list'))

    if request.method == 'POST':
        reminder.event_id = request.form['event_id']
        reminder.time = request.form['time']
        reminder.method = request.form['method']
        db.session.commit()
        return redirect(url_for('reminder_list'))

    return render_template('reminders.html', reminder=reminder)

@app.route('/delete_reminder/<int:reminder_id>')
def delete_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if reminder:
        db.session.delete(reminder)
        db.session.commit()

    return redirect(url_for('reminder_list'))
