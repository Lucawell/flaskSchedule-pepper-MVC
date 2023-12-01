# encoding:utf-8
from datetime import datetime
from app import db
from app.model.User import User


class EmailHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    recipients = db.Column(db.String(255), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, user_id, title, content, recipients):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.recipients = recipients
