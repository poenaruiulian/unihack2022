from flask import Flask
from datetime import timedelta

from db import db, db_init
from models import Users

app = Flask(__name__)
app.permanent_session_lifetime=timedelta(days=5)
app.secret_key = "gameover"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

@app.route("/", methods=['GET','POST'])
def home():
    

@app.route("/login")
def login():

@app.route("/signup")
def signup():

@app.route("/profiles")
def profiles():