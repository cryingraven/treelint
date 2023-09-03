from flask import Flask,send_from_directory,render_template
from flask_oauthlib.provider import OAuth2Provider
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_mail import Mail
from config import config
from werkzeug.exceptions import HTTPException,NotFound
from flask_socketio import SocketIO
from pymongo import MongoClient
import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/config/config.json'
# pylint: disable=C0103
app = Flask(__name__)
app.secret_key=config['SECRET']
app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DB_URL']
app.config['MAIL_SERVER'] = config['MAIL_SERVER']
app.config['MAIL_PORT'] = config['MAIL_PORT']
app.config['MAIL_USE_TLS'] = config['MAIL_USE_TLS']
app.config['MAIL_USERNAME'] = config['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config['MAIL_PASSWORD']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['SQLALCHEMY_TRACK_MODIFICATIONS']
login=LoginManager()
login.init_app(app)
login.login_view="login"
db=SQLAlchemy(app)
migrate=Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
oauth = OAuth2Provider(app)
socketio=SocketIO()
mail=Mail(app)
storage = storage.Client()
mongo=MongoClient(host=config['MONGO_SERVER'],port=config['MONGO_PORT'])['treelint']


