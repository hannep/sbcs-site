from application import app
from flask import Flask, request
from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user, logout_user
from sbcswebsite.models import Announcement, JobPost, BlogPost

@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/calendar")
def calendar(): 
    return render_template("calendar.html")

@app.route("/announcements")
def announcements(): 
    announcement_list = Announcement.query.order_by(Announcement.id.desc()).limit(10).all() 
    return render_template("announcements.html", announcements=announcement_list)

@app.route("/jobs")
def jobs(): 
    job_post_list = JobPost.query.order_by(JobPost.id.desc()).limit(10).all() 
    return render_template("jobs.html", job_posts=job_post_list)

@app.route("/blog")
def blog(): 
    blog_post_list = BlogPost.query.order_by(BlogPost.id.desc()).limit(10).all() 
    return render_template("blog.html", blog_posts=blog_post_list)
