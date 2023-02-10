from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(10))
    name = db.Column(db.String(20))
