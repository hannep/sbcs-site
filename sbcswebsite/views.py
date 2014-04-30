from application import app
from flask import Flask, request, session
from flask import render_template, redirect, url_for
from flask.ext.login import login_user, login_required, current_user
from sbcswebsite.models import JobPost, NewsPost, Question, Answer, Tag, User, db, question_tag_table, job_post_tag_table, news_post_tag_table
from base64 import urlsafe_b64encode as b64encode, urlsafe_b64decode as b64decode
import requests
import os
import urlparse
import facebook
from sbcswebsite.users import admin_required
from datetime import datetime

@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/calendar")
def calendar(): 
    return render_template("calendar.html")

@app.route("/news")
def news(): 
    newsletter_list = NewsPost.query.order_by(NewsPost.id.desc()).limit(10).all() 
    tags = _tags_for_type(NewsPost, news_post_tag_table, "news_post_tag")
    return render_template("news.html", news_posts=newsletter_list, tags=tags)

@app.route("/news/tags/<tag>")
def news_post_tag(tag):
    news_posts = JobPost.query.join(job_post_tag_table).join(Tag).filter(Tag.tag == tag).order_by(JobPost.id.desc()).limitI(10).all()
    tags = _tags_for_type(NewsPost, news_post_tag_table, "news_post_tag")
    return render_template("news.html", news_posts=news_posts, tags=tags)

def _tag_from_cols(tup, tag_route):
    id, name, frequency = tup
    tag = Tag()
    tag.id = id
    tag.tag = name
    tag.frequency = frequency
    print name
    tag.url = url_for(tag_route, tag=name)
    return tag

def _tags_for_type(table, join_table, tag_route):
    tags_with_frequency = db.session.query(Tag.id, Tag.tag, db.func.count(Tag.id)).join(join_table).join(table).group_by(Tag.id).all()
    return [_tag_from_cols(tup, tag_route) for tup in tags_with_frequency if tup[2] > 0]

@app.route("/jobs")
def jobs(): 
    job_post_list = JobPost.query.order_by(JobPost.id.desc()).limit(10).all() 
    tags = _tags_for_type(JobPost, job_post_tag_table, "job_post_tag")
    return render_template("jobs.html", job_posts=job_post_list, tags=tags)

@app.route("/jobs/tags/<tag>")
def job_post_tag(tag):
    job_posts = JobPost.query.join(job_post_tag_table).join(Tag).filter(Tag.tag == tag).order_by(JobPost.id.desc()).limit(10).all()
    tags = _tags_for_type(JobPost, job_post_tag_table, "job_post_tag")
    return render_template("jobs.html", job_posts=job_posts, tags=tags)

@app.route("/ask/tags/<tag>")
def ask_tag(tag):
    questions = Question.query.join(question_tag_table).join(Tag).filter(Tag.tag == tag).order_by(Question.touched_date.desc()).limit(10).all()
    tags = _tags_for_type(Question, question_tag_table, "ask_tag")
    return render_template("ask.html", questions=questions, can_ask=False, tags=tags)

@app.route("/ask")
def ask(): 
    questions = Question.query.order_by(Question.touched_date.desc()).limit(10).all()
    tags = _tags_for_type(Question, question_tag_table, "ask_tag")
    return render_template("ask.html", questions=questions, can_ask=True, tags=tags)

def _get_tags_for_request(existing_tags = None):
    existing_tags = existing_tags or []
    request_tags = request.form.get("tags").split(",")
    db_tags = Tag.query.filter(Tag.tag.in_(request_tags)).all()
    old_tags = db_tags + existing_tags
    old_tag_words = set([tag.tag for tag in old_tags])
    new_tags = [Tag(tag=tag) for tag in request_tags if tag not in old_tag_words]
    return old_tags + new_tags

@app.route("/post_question", methods=["POST"])
@login_required
def post_question():
    question = Question()
    question.title = request.form.get("title")
    question.content = request.form.get("content")
    question.tags = _get_tags_for_request()
    question.touched_date = datetime.utcnow()
    question.user_id = current_user.id
    db.session.add(question)
    db.session.commit()
    return redirect(url_for("ask"))

@app.route("/post_answer", methods=["POST"])
@login_required
def post_answer():
    question = Question.query.get(request.form.get("question_id"))
    answer = Answer()
    answer.user_id = current_user.id
    answer.content = request.form.get("content")
    answer.question_id = question.id
    question.touched_date = datetime.utcnow()
    question.tags = _get_tags_for_request(question.tags)
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

