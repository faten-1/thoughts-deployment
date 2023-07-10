from flask import render_template,redirect,session,flash,request
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if 'user_id' in session:
        return redirect('/thoughts')
    return render_template("index.html")


@app.route("/register",methods=["POST"])
def register():
    if not User.validation_registration(request.form):
        return redirect('/')
    User.register(request.form)
    return redirect ('/thoughts')


@app.route('/login',methods = ['POST'])
def login():
    if not User.validation_login(request.form):
        return redirect('/')
    return redirect ('/thoughts')

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')
