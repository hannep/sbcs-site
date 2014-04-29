from sbcswebsite.application import app
from flask_wtf.csrf import CsrfProtect
from flask_wtf import Form
from wtforms import TextField, SubmitField, StringField
from wtforms.validators import DataRequired

CsrfProtect(app)