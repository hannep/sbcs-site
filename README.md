sbcs-site
=========
This package runs the SBCS website. It is a simple Flask package, and should be installable and runnable anywhere that supports mod_wsgi.

## Running in Debug.

Simply fun 'debug.py' after installing the dependencies for this package, and everything should work. This will use the settings in 'default_settings.py', which are not suitable for production.

## Installing on Apache

1.  First, you need to install the website using 'python setup.py install'. You can do this globally, or in a virtualenv, but if you do it in a virtualenv you'll have to point mod_wsgi at it. 
2.  Create a config file, that should just be a python file with the basic flask configuration that you want. Mostly this will involve setting up a SECRET_KEY value and a database connection string for SQLAlchemy (note that this has only been tested on SQLite databases).
3. Set up your Apache VirtualHost to use mod_wsgi and point it at the site. The 'application.wsgi' file represents a sample wsgi file that you can use to run the application once you have set up Apache. You will probably also want to serve the static folder using Apache, which can be done by symlinking to the installed static files.
4.  Point Apache mod_wsgi at the config file using 'SetEnv SBCSWEBSITE_SETTINGS' in your VirtualHosts config for apache.

