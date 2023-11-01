from app import db
from app.model.Event import Event


class Reminder(db.Model):
    __tablename__ = 'reminders'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey(Event.id, ondelete='CASCADE'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    method = db.Column(db.String(255), nullable=False)

    def __init__(self, event_id, time, method):
        self.event_id = event_id
        self.time = time
        self.method = method

    def __repr__(self):
        return '<Reminder %r>' % self.event_id
