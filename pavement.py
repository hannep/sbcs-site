from paver.easy import task, needs
from paver.setuputils import setup

from distutils.command.build import build
from setuptools import find_packages
import os.path
import subprocess

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

@task
@needs("build", "setuptools.command.install")
def install():
    pass

@task
@needs("build", "setuptools.command.develop")
def develop():
    pass