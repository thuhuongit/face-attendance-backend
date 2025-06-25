from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='employee')  # admin / employee
    avatar = db.Column(db.String(255), default='')
    salary_rate = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role,
            'avatar': self.avatar,
            'salary_rate': self.salary_rate,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

class AttendanceLog(db.Model):
    __tablename__ = 'attendance_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=False)
    check_out_time = db.Column(db.DateTime)
    salary = db.Column(db.Float, default=0.0)

    user = db.relationship("User", backref="attendance_logs")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'check_in_time': self.check_in_time.isoformat(),
            'check_out_time': self.check_out_time.isoformat() if self.check_out_time else None,
            'salary': self.salary
        }

class SalaryLog(db.Model):
    __tablename__ = 'salary_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours_worked = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref='salary_logs')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat(),
            'hours_worked': self.hours_worked,
            'amount': self.amount
        }

class MailLog(db.Model):
    __tablename__ = 'logs_sent_mail'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200))
    content = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='mail_logs')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'email': self.email,
            'subject': self.subject,
            'content': self.content,
            'sent_at': self.sent_at.isoformat()
        }
