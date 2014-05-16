from sbcswebsite.application import app
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    facebook_user_id = db.Column(db.BigInteger, unique=True)
    name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    def is_administrator(self):
        return self.is_admin

    def __str__(self):
        return self.name

job_post_tag_table = db.Table('job_post_tag', db.metadata,
    db.Column('job_post_id', db.Integer, db.ForeignKey('job_post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

news_post_tag_table = db.Table('news_post_tag', db.metadata,
    db.Column('news_post_id', db.Integer, db.ForeignKey('news_post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class NewsPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content_html = db.Column(db.Text)

    tags = db.relationship("Tag",
                secondary=news_post_tag_table,
                lazy="subquery")

    def __repr__(self):
        return '<BlogPost %r>' % self.title


class JobPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content_html = db.Column(db.Text)

    tags = db.relationship("Tag",
                secondary=job_post_tag_table,
                lazy="subquery")

    def __repr__(self):
        return '<JobPost %r>' % self.title

question_tag_table = db.Table('question_tag', db.metadata,
    db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(40), unique=True)

    def __str__(self):
        return self.tag

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(40), unique=True)
    expiration_date = db.Column(db.DateTime)

    def __str__(self):
        return self.access_token

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    touched_date = db.Column(db.DateTime)
    answers = db.relationship("Answer",
                    lazy="subquery"
        );

    tags = db.relationship("Tag",
                    secondary=question_tag_table,
                    backref="questions",
                    lazy="subquery")

    user = db.relationship("User",
                lazy="subquery"
        )

    def __repr__(self):
        return '<Question %r>' % self.title

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    question_id = db.Column('question_id', db.Integer, db.ForeignKey("question.id"), nullable=False)

    user = db.relationship("User",
                lazy="subquery"
        )

    def __str__(self):
        return "Answer {}: {}".format(self.id, self.content[:20])

    def __repr__(self):
        return '<Answer %r>' % self.id
