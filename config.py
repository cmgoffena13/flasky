import os
from dotenv import load_dotenv


base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, ".env"))
load_dotenv(os.path.join(base_dir, ".flaskenv"))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG") or 0
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(base_dir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMIN = os.environ.get("ADMIN")

    POSTS_PER_PAGE = int(os.environ.get("POSTS_PER_PAGE", 25))

    LANGUAGES = ["en", "es"]

    MS_TRANSLATOR_KEY = os.environ.get("MS_TRANSLATOR_KEY")

    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")

    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")

    REDIS_URL = os.environ.get("REDIS_URL") or "redis:///"
