from application import app
from flask import Flask, request, session
from flask import render_template, redirect, url_for
from flask.ext.login import login_user
from sbcswebsite.models import Announcement, JobPost, BlogPost, Question, Answer, Tag, User, db
from base64 import urlsafe_b64encode as b64encode, urlsafe_b64decode as b64decode
import requests
import os
import urlparse
import facebook
from sbcswebsite.facebooktools import require_login, user_id
from datetime import datetime

@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/calendar")
def calendar(): 
    return render_template("calendar.html")

@app.route("/news")
def news(): 
    newsletter_list = Announcement.query.order_by(Announcement.id.desc()).limit(10).all() 
    return render_template("news.html", newsletter=newsletter_list)

@app.route("/jobs")
def jobs(): 
    job_post_list = JobPost.query.order_by(JobPost.id.desc()).limit(10).all() 
    return render_template("jobs.html", job_posts=job_post_list)

@app.route("/jobs/edit")
@app.route("/jobs/edit/<job_id>")
def edit_job(job_id = None): 
    job_post_list = JobPost.query.order_by(JobPost.id.desc()).limit(10).all() 
    return render_template("job-edit.html", job_posts=job_post_list)

@app.route("/jobs/post", methods=["POST"])
def post_job():
    job = Job()
    return "hi"


@app.route("/blog")
def blog(): 
    blog_post_list = BlogPost.query.order_by(BlogPost.id.desc()).limit(10).all() 
    return render_template("blog.html", blog_posts=blog_post_list)

@app.route("/ask")
def ask(): 
    questions = Question.query.order_by(Question.touched_date.desc()).limit(10).all()

    return render_template("ask.html", questions=questions)

@app.route("/post_question", methods=["POST"])
@require_login
def post_question():
    question = Question()
    question.title = request.form.get("title")
    question.content = request.form.get("content")
    question.tags = [Tag(tag=tag) for tag in request.form.get("tags").split(",")]
    question.touched_date = datetime.utcnow()
    question.facebook_user_id = user_id()
    db.session.add(question)
    db.session.commit()
    return redirect(url_for("ask"))

@app.route("/post_answer", methods=["POST"])
@require_login
def post_answer():
    question = Question.query.get(request.form.get("question_id"))
    answer = Answer()
    answer.facebook_user_id = user_id()
    answer.content = request.form.get("content")
    answer.question_id = question.id
    question.touched_date = datetime.utcnow()
    db.session.add(question)
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for("ask"))

@app.route("/login")
def login():
    oauth_state = b64encode(os.urandom(32))
    session["oauth_state"] = oauth_state
    return redirect(
        "https://www.facebook.com/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&state={state}&scope={scope}"
        .format(
            app_id = app.config["FACEBOOK_APP_ID"],
            redirect_uri = url_for("finish_login", _external=True),
            state=oauth_state,
            scope="user_groups"
        )
    )

@app.route("/finish_login")
def finish_login():
    arg_state = request.args.get("state")
    if arg_state is not None and arg_state != session.get("oauth_state"):
        redirect(url_for("login"))
    code = request.args.get("code")
    if code is None:
        redirect(url_for("login"))
    base_url = "https://graph.facebook.com/oauth/access_token"
    url = "{base}?client_id={app_id}&redirect_uri={redirect_uri}&client_secret={app_secret}&code={code}&scope={scope}".format(
        base = base_url,
        app_id = app.config["FACEBOOK_APP_ID"],
        app_secret = app.config["FACEBOOK_APP_SECRET"],
        redirect_uri = url_for("finish_login", _external=True),
        code = code,
        scope = "user_groups"
    )
    response = requests.get(url)
    if not response.text.startswith("access_token"):
        return "Invalid login", 400
    parsed_response = urlparse.parse_qs(response.text)

    access_token = parsed_response["access_token"][0]
    graph = facebook.GraphAPI(access_token)
    group_ids = [int(group[u"id"]) for group in graph.get_connections("me", "groups")[u"data"]]
    print group_ids
    if app.config["SBCS_GROUP_ID"] not in group_ids:
        return "Not in facebook group", 400
    
    me = graph.get_object("me")
    facebook_id = int(me[u"id"])
    user = User.query.filter(User.facebook_user_id == facebook_id).scalar()
    if user == None:
        user = User()
        user.facebook_user_id = facebook_id
        user.name = me[u"name"]
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for("ask"))

