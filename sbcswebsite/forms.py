from sbcswebsite.application import app
from flask_wtf.csrf import CsrfProtect

CsrfProtect(app)