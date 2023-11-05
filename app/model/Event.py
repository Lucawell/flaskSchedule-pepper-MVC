from app import db
from app.model.User import User
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_property

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    event_time = db.Column(db.Time)
    end_date = db.Column(db.Date)
    location = db.Column(db.String(255))
    description = db.Column(db.String(255))
    repeat = db.Column(db.String(255), nullable=False, default="none")  # Text field for custom repeat types
    reminder_type = db.Column(db.String(255), nullable=False, default="none")
    reminder_time = db.Column(db.Float, nullable=True)

    @hybrid_property
    def duration(self):
        return self.end_date - self.start_date

    def __init__(self, user_id, title, start_date, event_time, end_date, location, description, reminder_time,
                 repeat, reminder_type):
        self.user_id = user_id
        self.title = title
        self.start_date = start_date
        self.event_time = event_time
        self.end_date = end_date
        self.location = location
        self.description = description
        self.repeat = repeat
        self.reminder_type = reminder_type
        self.reminder_time = reminder_time

    def __repr__(self):
        return '<Event %r>' % self.title
