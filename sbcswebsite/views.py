from application import app
from flask import Flask, request
from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user, logout_user

import sbcswebsite.auth

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

@app.route("/admin")
@login_required
def admin():
    return "YOU ARE LOGGED IN"

#TODO: Maybe add XSRF protection for this endpoint. Not a big security risk
@app.route("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated():
        return redirect(url_for('admin'))
    if request.method == 'POST':
        if sbcswebsite.auth.login(request.form['username'], request.form['password']):
            return redirect(url_for('admin'))
        else:
            error = 'Invalid username/password'
    return render_template("login.html")

