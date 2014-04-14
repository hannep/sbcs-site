from sbcswebsite.application import app
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content_html = db.Column(db.Text)

    def __repr__(self):
        return '<Announcement %r>' % self.title

class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content_html = db.Column(db.Text)

    def __repr__(self):
        return '<Announcement %r>' % self.title


class JobPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content_html = db.Column(db.Text)

    def __repr__(self):
        return '<Announcement %r>' % self.title

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facebook_user_id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    touched_date = db.Column(db.DateTime)

    def __repr(self):
        return '<Question %r>' % self.title

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facebook_user_id = db.Column(db.Integer)
    content = db.Column(db.Text)
    question_id = db.Column('question_id', db.Integer, nullable=False)

    def __repr(self):
        return '<Answer %r>' % id