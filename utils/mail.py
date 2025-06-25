from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_email(to, subject, body):
    with current_app.app_context():
        msg = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=[to])
        msg.body = body
        mail.send(msg)
