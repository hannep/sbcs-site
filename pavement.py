from paver.easy import task, needs
from paver.setuputils import setup

from distutils.command.build import build
from setuptools import find_packages
import os.path
import subprocess
import os, sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

@task
def initialize():
    import sbcswebsite.initialization as initlib
    initlib.initialize(os.getcwd())

@task
def init_db():
    from sbcswebsite.models import db
    db.create_all()

@task
def build_css():
    css_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "sbcswebsite/static/css")
    subprocess.check_call(["lessc", os.path.join(css_dir, "main.less"), os.path.join(css_dir, "main.css")])

@task
@needs("build_css")
def build():
    pass

@task
@needs("build")
def init_site():
    initialize(os.getcwd())