from app import app
from flask_login import login_required,current_user
from flask import render_template
from model import TApp
@app.route('/')
@login_required
def index():
    app = TApp.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html',apps=app)