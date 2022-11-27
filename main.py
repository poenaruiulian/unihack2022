from flask import Flask,flash,session,request,redirect,url_for,render_template
from datetime import timedelta
import bcrypt
import base64

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
                return redirect(url_for("dashboard"))
        else:
            message = "The passwords don't match,Try again."

    if message != None:
        flash(message)
    return render_template("register.html")



@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    if 'userInSession' in session:
        cardsToShow = UsersCards.query.filter_by(mail=session['userInSession']).all()
        
        if request.method == "POST":
            cardToDelete = request.form["delete"]
            print(cardToDelete)

            deleteCard = UsersCards.query.filter_by(mail =session['userInSession']).filter_by(cardName=cardToDelete).first()
            db.session.delete(deleteCard)
            db.session.commit()
            
            
            try: 
                for i in range(5):
                    deleteLink = Link.query.filter_by(cardName=cardToDelete).first()  
                    db.session.delete(deleteLink)
            except:
                pass

            return redirect(url_for("dashboard"))

            
    else: redirect(url_for("login"))

    return render_template("dashboard.html", cardsToShow = cardsToShow, length = len(cardsToShow))

@app.route("/create_card", methods=['GET','POST'])
def create_card():
    if 'userInSession' in session:
        if request.method == 'POST':

            cardName = request.form["cardName"]
            displayName = request.form["displayName"]
            profilePic = request.files["profilePic"]

            cardName = cardName.split(" ")
            copy = ""
            for i in cardName: copy+=i
            cardName=copy

            mimetype = profilePic.mimetype

            addCard = UsersCards(
                mail = session['userInSession'],
                cardName = cardName,
                displayName = displayName,
                profilePic = profilePic.read(),
                profileMim = mimetype
            )

            db.session.add(addCard)
            db.session.commit()

            for i in range(1,6):
                lT = request.form["linkTitle{}".format(i)]
                lB = request.form["linkBody{}".format(i)]
                lP = request.files["linkPic{}".format(i)]

                mimetype = lP.mimetype
                print(lP)
                addLink = Link(
                    mail = session['userInSession'],
                    cardName = cardName,
                    linkName = lT,
                    link = lB,
                    linkPic = lP.read(),
                    linkMim = mimetype
                )
                if lT != '':
                    db.session.add(addLink)
                    db.session.commit()

            return redirect(url_for("dashboard"))

    else: return redirect(url_for("login"))

    return render_template("createCard.html")

@app.route("/card/<cn>", methods=['GET','POST'])
def card(cn):
    if 'userInSession' in session:
        selectCard = UsersCards.query.filter_by(cardName = cn).filter_by(mail=session['userInSession']).first()
        selectLinks = Link.query.filter_by(cardName = cn).filter_by(mail=session['userInSession']).all()
        linksName = []
        linksLink = []
        linksImg = []
        linksMim = []
        k=0
        for i in selectLinks:
            linksName.append(i.linkName)
            linksLink.append(i.link)
            linksImg.append(i.linkPic)
            linksMim.append(i.linkMim)
            k+=1
        
        return render_template("card.html", card=selectCard,user=session['userInSession'] ,base64=base64,names=linksName, links=linksLink, imgs=linksImg, mims=linksMim, k=k)
    else: return redirect(url_for("login"))

@app.route("/<user>/<cn>",methods=['GET','POST'])
def share(user,cn):
    selectCard = UsersCards.query.filter_by(cardName = cn).filter_by(mail=user).first()
    selectLinks = Link.query.filter_by(cardName = cn).filter_by(mail=user).all()

    linksName = []
    linksLink = []
    linksImg = []
    linksMim = []
    k=0
    for i in selectLinks:
        linksName.append(i.linkName)
        linksLink.append(i.link)
        linksImg.append(i.linkPic)
        linksMim.append(i.linkMim)
        k+=1
        
    return render_template("share.html", card=selectCard,user=session['userInSession'] ,base64=base64,names=linksName, links=linksLink, imgs=linksImg, mims=linksMim, k=k)

@app.route("/signout")
def signout():
    if "userInSession" in session:
        session.pop("userInSession", None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

if __name__== "__main__":
 
    app.run(debug=True)