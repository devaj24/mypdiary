from flask import current_app
from datetime import datetime
from mydiary import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    dp = db.Column(db.String(), default='default.jpg')
    activated = db.Column(db.Boolean, default=False)
    pages = db.relationship('Page', backref='author', lazy=True)

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.dp})'

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=False) 
    image = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Page({self.title} on {self.date_posted})'

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text) 

    def __repr__(self):
        return f'{self.id}, {self.rating} , {self.feedback}'

class Support(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'{self.id}, {self.answer}'