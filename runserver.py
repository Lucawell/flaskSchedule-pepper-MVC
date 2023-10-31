from app import app
from app.model.User import User
from app.model.Event import Event
from app.model.Reminder import Reminder
from flask import render_template

@app.route('/')
def index():
    users = User.query.all()
    events = Event.query.all()
    reminders = Reminder.query.all()

    return render_template('index.html', users=users, events=events, reminders=reminders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


