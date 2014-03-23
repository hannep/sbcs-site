import flask
from flask import Flask
from flask import render_template  
from base64 import urlsafe_b64encode as b64encode

import datetime
import os

import sbcs_settings

app = Flask(__name__)

app.config.from_envvar('SBCSWEBSITE_SETTINGS', silent=True)

#Shamelessly stolen from http://flask.pocoo.org/snippets/3/
@app.before_request
def csrf_protect():
    if flask.request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != flask.request.form.get('_csrf_token'):
            abort(400)

def generate_csrf_token():
    if '_csrf_token' not in flask.session:
        flask.session['_csrf_token'] = b64encode(os.urandom(24))
    return flask.session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token 

@app.route("/")
def index(): 
	return render_template("index.html")

@app.route("/calendar")
def calendar(): 
	return render_template("calendar.html")

@app.route("/announcements")
def announcements(): 
	return render_template("announcements.html")

@app.route("/jobs")
def jobs(): 
	return render_template("jobs.html")

@app.route("/blog")
def blog(): 
	return render_template("blog.html")

@app.route("/admin/login")
def admin_login():
    return app.secret_key
    return render_template("login.html")

