import os
from flask import Flask
from .db import init_app
from . import auth # using "." or "flaskr" means the same when importing a module
from . import blog

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    print(f"Name of current python module: {__name__}")
    print(f"Path that flask has chosen for the instance folder {app.instance_path}")
    app.config.from_mapping(
        SECRET_KEY="dev",# Used to keep data safe
        DATABASE=os.path.join(app.instance_path,"flaskr.sqlite")
    )
    print(test_config)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"
    
    init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule(rule="/", endpoint="index")

    return app


