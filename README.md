sbcs-site
=========
This package runs the SBCS website. It is a simple Flask package, and should be installable and runnable anywhere that supports mod_wsgi.

## Running in Debug.

`python setup.py install
sbcswebsite_init.py
sbcswebsite_db.py
python debug.py`

## Installing on Apache

1.  First, you need to install the website using 'python setup.py install'. You can do this globally, or in a virtualenv, but if you do it in a virtualenv you'll have to point mod_wsgi at it. 
2.  Run sbcswebsite_init.py to initialize a skeleton directory, which will include a folder for media, a symlink to the static files, a sample wsgi file, and an example config file
3. Set up your Apache VirtualHost to use mod_wsgi and point it at the site. The 'application.wsgi' file represents a sample wsgi file that you can use to run the application once you have set up Apache. You will probably also want to serve the static and media folders using Apache
4.  Point Apache mod_wsgi at the config file using 'SetEnv SBCSWEBSITE_SETTINGS' in your VirtualHosts config for apache.

