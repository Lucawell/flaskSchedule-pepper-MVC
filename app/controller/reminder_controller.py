from flask_mail import Message
from app import mail

def send_email(subject, html, recipients):
    msg = Message(subject, recipients=recipients, html=html)
    mail.send(msg)
