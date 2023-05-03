import json
from . import  db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String(150), unique=True)
    buffertime = db.Column(db.DateTime(timezone=True))
    bufferattempts = db.Column(db.Integer)
    goat = db.Column(db.String(150))
    stats = db.relationship('Stats', backref='user', uselist=False)

class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)
    times = db.Column(db.String)
    sumoftimes = db.Column(db.Integer)
    attempts = db.Column(db.String)
    sumofattempts = db.Column(db.Integer)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False, unique=True)
