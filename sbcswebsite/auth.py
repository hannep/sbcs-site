from sbcswebsite.application import app
from passlib.hash import bcrypt
from flask.ext.login import LoginManager, login_user

from sbcswebsite.models import User

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()

def login(username, password):
    user = load_user(username)
    if user is None:
        return False
    if bcrypt.verify(password, user.password):
        return login_user(user)
    return False