import os
from dotenv import load_dotenv

import src.factory as factory
import src.models.persistent.data_generator as data_generator

app = factory.create_app()

if __name__ == "__main__":
    load_dotenv()

    app.secret_key = os.environ.get("SECRET_KEY")

    app.config["DEBUG"] = os.environ.get("DEBUG") == "1"

    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME")
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"mysql+pymysql://{db_user}:{db_pass}@localhost/{db_name}"

    refresh_db = os.environ.get("REFRESH_DB") == "1"
    if refresh_db:
        data_generator.generate_sample_data()

    # app.run(ssl_context="adhoc")
    app.run()
