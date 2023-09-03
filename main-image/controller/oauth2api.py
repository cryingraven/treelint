from app import app,oauth
@app.route('/test')
@oauth.require_oauth('user-app')
def test():
    return "OK"
