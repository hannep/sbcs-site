from application import app
from users import admin_required
from models import db, JobPost, NewsPost, Question, Answer, Tag, Token

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin, AdminIndexView
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user
import flask_wtf

class HiddenAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_administrator()


class CsrfModelView(ModelView):
    form_base_class = flask_wtf.Form
    def is_accessible(self):
        return current_user.is_administrator()

admin = Admin(app, index_view=HiddenAdminView())
admin.add_view(CsrfModelView(JobPost, db.session))
admin.add_view(CsrfModelView(NewsPost, db.session))
admin.add_view(CsrfModelView(Question, db.session))
admin.add_view(CsrfModelView(Answer, db.session))
admin.add_view(CsrfModelView(Tag, db.session))
admin.add_view(CsrfModelView(Token, db.session))
