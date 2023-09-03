from app import socketio
import functools
from flask_login import current_user
from flask_socketio import disconnect

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

@socketio.on('initApp')
@authenticated_only
def initApp(appID, methods=['GET', 'POST']):
    socketio.join(appID)
    socketio.emit('progress',{})
