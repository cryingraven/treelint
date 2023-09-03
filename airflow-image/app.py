from flask import Flask,send_from_directory
from src.config import config
app = Flask(__name__)
@app.route('/source/<path:path>')
def send_css(path):
    return send_from_directory('source/', path)