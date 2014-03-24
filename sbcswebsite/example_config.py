import os

_dir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
APP_SECRET = "CHANGE THIS"
SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(os.path.join(_dir, "test.db"))
