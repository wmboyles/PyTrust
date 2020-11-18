"""
This is the main file that creates and runs the app.
It must be named app.py for the flask run command to work.

:author William Boyles:
"""

from flask import Flask
from dotenv import load_dotenv
import os

import src.models.persistent.persistent as persistent
import src.view_controllers.view_controllers as view_controllers
import src.api_controllers.api_controllers as api_controllers
import src.models.persistent.data_generator as data_generator


def create_app(refresh_db=False):
    app = Flask(__name__)

    # Get all our secrets as environment variables
    load_dotenv()

    app.secret_key = os.environ.get("SECRET_KEY")

    app.config["DEBUG"] = os.environ.get("DEBUG") == "1"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
        os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") == "1"
    )

    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME")
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"mysql+pymysql://{db_user}:{db_pass}@localhost/{db_name}"

    persistent.db.init_app(app)
    persistent.ma.init_app(app)

    for view_blueprint in view_controllers.view_controllers:
        app.register_blueprint(view_blueprint, url_prefix=view_controllers.BASE_URL)

    for api_blueprint in api_controllers.api_controllers:
        app.register_blueprint(api_blueprint, url_prefix=api_controllers.BASE_URL)

    app.app_context().push()

    if refresh_db:
        data_generator.generate_sample_data()

    return app