from flask import Flask
from flask import render_template  
app = Flask(__name__, static_folder=None)

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
