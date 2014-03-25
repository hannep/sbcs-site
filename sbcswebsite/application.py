import flask
from flask import Flask, request
from flask import render_template, redirect, url_for
from base64 import urlsafe_b64encode as b64encode

import datetime
import os
import sbcswebsite.config

app = Flask("sbcswebsite")
app.config.from_object(sbcswebsite.config.config)

#Shamelessly stolen from http://flask.pocoo.org/snippets/3/
@app.before_request
def csrf_protect():
    if flask.request.method == "POST":
        token = flask.session.get('_csrf_token', None)
        if not token or token != flask.request.form.get('_csrf_token'):
            abort(400)

def generate_csrf_token():
    if '_csrf_token' not in flask.session:
        flask.session['_csrf_token'] = b64encode(os.urandom(24))
    return flask.session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token 
