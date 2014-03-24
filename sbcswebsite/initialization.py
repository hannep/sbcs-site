import os
import shutil
import textwrap
package_dir = os.path.abspath(os.path.dirname(__file__))

def initialize(directory):
    global package_dir
    target_config = os.path.join(directory, 'sbcswebsite_config.py')
    if not os.path.exists(target_config):
        shutil.copyfile(os.path.join(package_dir, 'example_config.py'), target_config)
    wsgi_file = os.path.join(directory, 'application.wsgi')
    if not os.path.exists(wsgi_file):
        with open(wsgi_file, "w") as outfile:
            outfile.write("from sbcswebsite.application import app as application\n")

    debug_file = os.path.join(directory, 'debug.py')
    if not os.path.exists(debug_file):
        with open(debug_file, "w") as outfile:
            outfile.write(textwrap.dedent(
                """
                from sbcswebsite.application import app
                app.run()
                """
            ))
    media_dir = os.path.join(directory, "media")
    if not os.path.exists(media_dir):
        os.mkdir(media_dir)
    static_dir = os.path.join(package_dir, "static")
    if not os.path.exists(static_dir):
        os.symlink(static_dir, os.path.join(directory, "static"))



