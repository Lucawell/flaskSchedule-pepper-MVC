from app import db
from app.model.User import User


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def __init__(self, user_id, title, start_time, end_time, location, description):
        self.user_id = user_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.description = description

    def __repr__(self):
        return '<Even %r>' % self.user_id
