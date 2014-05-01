from sbcswebsite.application import app
from models import User
from flask.ext.login import LoginManager, current_user
from functools import wraps
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated():
            return login_manager.unauthorized()
        if not current_user.is_administrator():
            return "Forbidden", 403
        return func(*args, **kwargs)
    return wrapper
