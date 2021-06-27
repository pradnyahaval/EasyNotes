#database models

from enum import unique
from . import db # . => from current folder 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(db.String(5000)) #notes upto 5000 characters
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #for primary key 'id'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False) #string of length 100
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100), nullable=False)
    notes = db.relationship('Note') #everytime we create a note, it will be added into this relationship

