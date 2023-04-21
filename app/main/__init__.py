from flask import Blueprint

bp = Blueprint(name='main', import_name=__name__)

from app.main import routes