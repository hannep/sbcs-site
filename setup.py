from setuptools import setup, find_packages
setup(
    name = "SBCS Site",
    version = "0.1",
    packages = find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = [
        'flask>=0.6',
        'Flask-SQLAlchemy>=1.0'
    ],

    # could also include long_description, download_url, classifiers, etc.
)