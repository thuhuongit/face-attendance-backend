from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    salary_per_hour = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)

class AttendanceLog(db.Model):
    __tablename__ = "attendance_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    check_type = db.Column(db.Enum('in', 'out'))
    timestamp = db.Column(db.DateTime, default=datetime.now)

class SalaryReport(db.Model):
    __tablename__ = "salary_reports"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    total_hours = db.Column(db.Float)
    total_salary = db.Column(db.Float)
