from flask import Blueprint

bp = Blueprint(name="auth", import_name=__name__)

from app.auth import routes
