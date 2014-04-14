from flask import session
from sbcswebsite.application import app
from functools import wraps

def is_logged_in():
    return "fb_id" in session

def user_id():
    return int(session["fb_id"])

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_logged_in():
            return func(*args, **kwargs)
        else:
            return "Not logged in", 400
    return wrapper

app.jinja_env.globals.update(is_fb_logged_in = is_logged_in)