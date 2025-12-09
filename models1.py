from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))
    probation = db.Column(db.Boolean, default=False)
    hire_date = db.Column(db.Date)
