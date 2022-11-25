from db import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    username = db.Column(db.Text, nullable = False)
    password = db.Column(db.Text, nullable = False)
    mail = db.Column(db.Text, nullable = False)