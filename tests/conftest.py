import pytest
from app import create_app, db
from config import Config


class TestConfig(Config):
    TESTING = (True,)
    SQLALCHEMY_DATABASE_URI = "sqlite:///"


@pytest.fixture(autouse=True)
def setUp_tearDown():
    print("Setting up test db")
    test_app = create_app(config_class=TestConfig)
    test_app_context = test_app.app_context()
    test_app_context.push()
    db.create_all()
    yield
    print("Tearing down test db")
    db.session.remove()
    db.drop_all()
    test_app_context.pop()
