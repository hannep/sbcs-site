from paver.easy import task, needs
from paver.setuputils import setup

from distutils.command.build import build
from setuptools import find_packages
import os.path
import subprocess

setup(
    name = "SBCS Site",
    version = "0.1",
    packages = find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = [
        'flask>=0.6',
        'Flask-SQLAlchemy>=1.0',
        'Flask-Login>=0.2.10',
        'passlib>=1.6.2',
    ],
    include_package_data = True,
    zip_safe = False,
    scripts = [
        'scripts/sbcswebsite_init.py',
        'scripts/sbcswebsite_announce.py',
        'scripts/sbcswebsite_blog.py',
        'scripts/sbcswebsite_job.py',
        'scripts/sbcswebsite_db.py'
    ],

    # could also include long_description, download_url, classifiers, etc.
)

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