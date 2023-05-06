from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.api.schemas import UserDataSchema, UserUpdateSchema, UserRegisterSchema
from app.models import User
from flask import jsonify


bp = Blueprint(name="users", import_name=__name__, description="Operations on Users")

# GET = SELECT
# POST = INSERT
# PUT = UPDATE
# DELETE = DELETE
@bp.route('/api/users/<int:user_id>')
class API_User(MethodView):

    @bp.response(200, UserDataSchema)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        user_data = jsonify(user.to_dict())
        return user_data

    @bp.arguments(UserUpdateSchema)
    @bp.response(200, UserDataSchema)
    def put(self, user_id):
        pass

@bp.route('api/users')
class API_Users(MethodView):

    @bp.response(200, UserDataSchema(many=True))
    def get(self):
        pass


@bp.route('/api/users/<int:user_id>/followers', methods=['GET'])
def get_followers(user_id):
    pass

@bp.route('/api/users/<int:user_id>/followed', methods=['GET'])
def get_followed(user_id):
    pass