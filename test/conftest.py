import os
from dotenv import load_dotenv
import pytest

from src.factory import create_app
from src.models.persistent.persistent import db as _db

load_dotenv()
TEST_DB_PATH = os.environ.get("TEST_DB_PATH")
TEST_DATABASE_URI = "sqlite:///" + TEST_DB_PATH


@pytest.fixture(scope="session")
def app(request):
    app = create_app()
    app.secret_key = os.environ.get("SECRET_KEY")
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DATABASE_URI

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def db(app, request):
    if os.path.exists(TEST_DB_PATH):
        os.unlink(TEST_DB_PATH)

    def teardown():
        _db.drop_all()
        os.unlink(TEST_DB_PATH)

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
