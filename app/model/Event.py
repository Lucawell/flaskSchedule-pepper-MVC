from app import db
from app.model.User import User
from enum import Enum
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property


class RepeatType(Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    description = db.Column(db.String(255))
    repeat = db.Column(db.Enum(RepeatType), nullable=False, default=RepeatType.NONE)

    reminder = db.relationship('Reminder', backref='event', lazy='dynamic')

    @hybrid_property
    def duration(self):
        return self.end_time - self.start_time

    def __init__(self, user_id, title, start_time, end_time, location, description, repeat=RepeatType.NONE):
        self.user_id = user_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.description = description
        self.repeat = repeat

    def __repr__(self):
        return '<Even %r>' % self.user_id
