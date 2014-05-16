from application import app
from users import admin_required
from models import db, JobPost, NewsPost, Question, Answer, Tag, Token

from flask import redirect,url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin, AdminIndexView, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user
import flask_wtf

from base64 import urlsafe_b64encode as b64encode, urlsafe_b64decode as b64decode
import os
#consider removing 'url_for'

class HiddenAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_administrator()

class FacebookWall(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/fb-login.html')

    def is_accessible(self):
        return current_user.is_administrator()

    @expose("/fb-login")
    def fb_login(self):
        redirect_url =  url_for("fb_complete", _external=True)
        oauth_state = b64encode(os.urandom(32))
        return redirect(
            "https://www.facebook.com/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&state={state}&scope={scope}".format(
                app_id = app.config["FACEBOOK_APP_ID"],
                redirect_uri = redirect_url,
                state=oauth_state,
                scope="user_groups"
            )
        )
    @expose("/fb-complete")
    def fb_complete(self):
       return self.render('admin/fb-complete.html')

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
admin.add_view(FacebookWall())
