from flask import Flask, current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy  # add
from datetime import datetime  # add
from app import db,login


class User(UserMixin, db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String())


    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


    def __repr__(self):
        return f'user: {self.username}'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Task(db.Model):
    __tablename__= 'task'
    id = db.Column(db.Integer, primary_key=True)
    track_no = db.Column(db.String(12), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    dates = db.Column(db.String(10), nullable=False)
    times = db.Column(db.String(10), nullable=False)
    received_by = db.Column(db.String(40), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def __repr__(self):
        return f'task: {self.name}'