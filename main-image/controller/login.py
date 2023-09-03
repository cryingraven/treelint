from app import app
from flask_login import logout_user,login_user
from flask import render_template,redirect,request,flash
from model import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/do_login', methods=['POST'])
def login_process():
    username=request.form.get('username')
    password=request.form.get('password')
    u=User.query.filter_by(username=username).first()
    if u is None or not password==u.password:
        flash('Invalid Username Password')
        return redirect("/login")
    login_user(u, remember=False)
    return redirect("/")

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
