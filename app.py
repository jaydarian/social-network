from flask import Flask, g
from flask.ext.login import LoginManager

import models

DEBUG = True
PORT = 8001
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'hu8n90l.m89c.v89d.234.f89d'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

if __name__ == '__main__':
    models.initialize()
    models.User.create_user(
                username='jaydarius',
                email='jayrey.go@gmail.com',
                password='password',
                admin = True
    )
    app.run(debug=DEBUG, host=HOST, port=PORT)