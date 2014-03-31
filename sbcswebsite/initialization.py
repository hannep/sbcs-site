import os
import shutil
import textwrap
package_dir = os.path.abspath(os.path.dirname(__file__))

def initialize(directory):
    global package_dir
    target_config = os.path.join(directory, 'sbcswebsite_config.py')
    if not os.path.exists(target_config):
        with open(target_config, "w") as outfile:
            outfile.write(textwrap.dedent("""
                import os

                _dir = os.path.abspath(os.path.dirname(__file__))
                DEBUG = True
                APP_SECRET = {0}
                SQLALCHEMY_DATABASE_URI = "sqlite:///{{0}}".format(os.path.join(_dir, "test.db"))
                """.format(repr(os.urandom(40)))))
    wsgi_file = os.path.join(directory, 'application.wsgi')
    if not os.path.exists(wsgi_file):
        with open(wsgi_file, "w") as outfile:
            outfile.write(textwrap.dedent("""
                import os
                os.environ["SBCSWEBSITE_CONFIG"] = os.environ.get("SBCSWEBSITE_CONFIG", None) or "{0}"
                from sbcswebsite.website import application
                """.format(target_config)))

    debug_file = os.path.join(directory, 'debug.py')
    if not os.path.exists(debug_file):
        with open(debug_file, "w") as outfile:
            outfile.write(textwrap.dedent(
                """
                from sbcswebsite.website import application
                application.run()
                """
            ))
    media_dir = os.path.join(directory, "media")
    if not os.path.exists(media_dir):
        os.mkdir(media_dir)
    static_dir = os.path.join(directory, "static")
    if not os.path.exists(static_dir):
        os.symlink(os.path.join(package_dir, "static"), static_dir)



