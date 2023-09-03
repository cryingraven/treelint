from app import app,socketio,login
from config import config
import model
import controller
from model import User

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
if __name__ == '__main__':
    socketio.init_app(app, async_mode='threading', message_queue=config['MSG_QUEUE'], logger=False, engineio_logger=False)
    socketio.run(app,debug=True, port=8080, host='0.0.0.0')