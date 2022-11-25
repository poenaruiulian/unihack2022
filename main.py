from flask import Flask,session,request,redirect,url_for,render_template
from datetime import timedelta

from db import db, db_init
from models import Users

app = Flask(__name__)
app.permanent_session_lifetime=timedelta(days=5)
app.secret_key = "gameover"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

userInSession = False

@app.route("/", methods=['GET','POST'])
def home():
    if userInSession == True:
        return redirect(url_for("dashboard"))
    else: 
        return render_template("login.html")

@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':

        session.permanent = True

        firstNameRegister = request.form["first_name"]
        lastNameRegister = request.form["last_name"]
        passRegister = request.form["passReg"]
        passRegisterVerif = request.form["passRegVerif"]
        mailRegister = request.form["mail"]




if __name__== "__main__":
    app.run(debug=True)