from db import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    password = db.Column(db.Text, nullable = False)
    mail = db.Column(db.Text, nullable = False)

class UsersCards(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    mail = db.Column(db.Text, nullable = False)
    cardName = db.Column(db.Text, nullable=False)
    displayName = db.Column(db.Text, nullable = False)
    profilePic = db.Column(db.Text, nullable = False)
    profileMim = db.Column(db.Text, nullable = False)
    
class Link(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    mail = db.Column(db.Text, nullable = False)
    cardName = db.Column(db.Text, nullable=False)
    linkName = db.Column(db.Text, nullable = False)
    link = db.Column(db.Text, nullable = False)
    linkPic = db.Column(db.Text, nullable = False)
    linkMim = db.Column(db.Text, nullable = False)