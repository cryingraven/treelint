from app import app
from flask_login import logout_user,login_user
from flask import render_template,redirect,request,flash
from model import User

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('forgot.html')