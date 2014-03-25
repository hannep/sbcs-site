from setuptools import setup, find_packages
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
        'bcrypt>=1.0.2',
    ],
    include_package_data = True,
    zip_safe = False,
    scripts = [
        'scripts/sbcswebsite_init.py',
        'scripts/sbcswebsite_announce.py',
        'scripts/sbcswebsite_blog.py',
        'scripts/sbcswebsite_job.py',
        'scripts/sbcswebsite_db.py'
    ]

    # could also include long_description, download_url, classifiers, etc.
)