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

