from sbcswebsite.application import app
from sbcswebsite.models import db

app.config.from_object('sbcswebsite.debug_settings')

db.create_all()