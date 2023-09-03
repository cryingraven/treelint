from app import app
from flask_login import logout_user,login_user
from flask import render_template,redirect,request,flash
from model import User

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')
@app.route('/do_register', methods=['POST'])
def do_register():
    username=request.form.get('username')
    password=request.form.get('password')
    cpassword=request.form.get('cpassword')
    fullname=request.form.get('fullname')
    email=request.form.get('email')
    return redirect("/register")
    if password==cpassword:
        flash('Password Not Match')
        return redirect("/register")
    return render_template('register.html')