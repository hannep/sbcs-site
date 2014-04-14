import flask
from flask import session, request
from base64 import urlsafe_b64encode as b64encode 
import os
from functools import wraps
from sbcswebsite.application import app


#Shamelessly stolen from http://flask.pocoo.org/snippets/3/
@app.before_request
def xsrf_protect():
    if flask.request.method == "POST":
        token = flask.session.get('_xsrf_token', None)
        if not token or token != flask.request.form.get('_xsrf_token'):
            abort(400)

def generate_xsrf_token():
    if '_xsrf_token' not in flask.session:
        flask.session['_xsrf_token'] = b64encode(os.urandom(24))
    return flask.session['_xsrf_token']

app.jinja_env.globals['xsrf_token'] = generate_xsrf_token 