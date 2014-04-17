from sbcswebsite.application import app
from models import User
from flask.ext.login import LoginManager
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)