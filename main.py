from flask import Flask,flash,session,request,redirect,url_for,render_template
from datetime import timedelta
import bcrypt

from db import db, db_init
from models import Users,UsersCards, Link


app = Flask(__name__)
app.permanent_session_lifetime=timedelta(days=5)
app.secret_key = "gameover"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

userInSession = False

@app.route("/login", methods=['GET','POST'])
def login():

    message = None

    if userInSession == True:
        return redirect(url_for("dashboard"))
    else: 

        if request.method=='POST':
            mailLogin = request.form["e-mail"]
            passLogin = request.form["password"]

            existUser = Users.query.filter_by(mail = mailLogin).first()
            if not existUser: message = "Try making an account!"
            else:
                if bcrypt.checkpw(passLogin.encode('utf-8'), existUser.password):
                    session["userInSession"] = mailLogin
                    message = "Now you are signed in!"
                    session.permanent = True
                    return redirect(url_for("dashboard"))
                else: message="Password incorect!"
        
    if message != None:
        flash(message)
    return render_template("login.html")

@app.route("/register", methods = ['POST', 'GET'])
def register():

    message = None

    if request.method == 'POST':

        
        session.permanent = True

        firstNameRegister = request.form["firstname"]
        lastNameRegister = request.form["lastname"]
        passRegister = request.form["password"]
        passRegisterVerif = request.form["cpassword"]
        mailRegister = request.form["e-mail"]

    

        existUser = Users.query.filter_by(mail = mailRegister).first()
        
        if passRegister==passRegisterVerif:
            if existUser: message = "This email allready exist!"
            else:
                hashed = bcrypt.hashpw(passRegister.encode('utf-8'), bcrypt.gensalt())

                addUser = Users(
                    first_name = firstNameRegister,
                    last_name = lastNameRegister,
                    password = hashed,
                    mail = mailRegister
                )

                db.session.add(addUser)
                db.session.commit()

                session['userInSession'] = mailRegister
                print()
                message = 'Welcome'
        else:
            message = "The passwords don't match,Try again."

    if message != None:
        flash(message)
    return render_template("register.html")



@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    if 'userInSession' in session:
        cardsToShow = UsersCards.query.filter_by(mail=session['userInSession']).all()
        print(cardsToShow)
    else: redirect(url_for("login"))

    return render_template("dashboard.html", cardsToShow = cardsToShow, length = len(cardsToShow))

@app.route("/create_card", methods=['GET','POST'])
def create_card():
    if 'userInSession' in session:
        if request.method == 'POST':

            cardName = request.form["cardName"]
            displayName = request.form["displayName"]
            profilePic = request.files["profilePic"]

            

            addCard = UsersCards(
                mail = session['userInSession'],
                cardName = cardName,
                displayName = displayName,
                profilePic = profilePic.read()
            )

            db.session.add(addCard)
            db.session.commit()

            linkTitle = request.form["linkTitle"]
            linkBody = request.form["link"]
            linkPic = request.files["linkPic"]

            addLink = Link(
                mail = session['userInSession'],
                linkName = linkTitle,
                link = linkBody,
                linkPic = linkPic.read()
            )

            db.session.add(addLink)
            db.session.commit()

    else: return redirect(url_for("login"))

    return render_template("createCard.html")

@app.route("/signout")
def signout():
    if "userInSession" in session:
        session.pop("userInSession", None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

if __name__== "__main__":
 
    app.run(debug=True)