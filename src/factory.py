"""
This is the main file that creates and runs the app.
It must be named app.py for the flask run command to work.

:author William Boyles:
"""

from flask import Flask

import src.models.persistent.persistent as persistent
import src.view_controllers.view_controllers as view_controllers
import src.api_controllers.api_controllers as api_controllers


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # will change. Here to suppress a warning
    app.config["SQLALCHEMY_DATABASE_URI"] = ""

    persistent.db.init_app(app)
    persistent.ma.init_app(app)

    for view_blueprint in view_controllers.view_controllers:
        app.register_blueprint(view_blueprint, url_prefix=view_controllers.BASE_URL)

    for api_blueprint in api_controllers.api_controllers:
        app.register_blueprint(api_blueprint, url_prefix=api_controllers.BASE_URL)

    app.app_context().push()

    return app
