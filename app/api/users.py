from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.api.schemas import UserDataSchema, UserUpdateSchema, UserRegisterSchema, UsersCollectionDataSchema
from app.models import User
from flask import jsonify, request


bp = Blueprint(name="users", import_name=__name__, description="Operations on Users")

# GET = SELECT
# POST = INSERT
# PUT = UPDATE
# DELETE = DELETE
@bp.route('/api/users/<int:user_id>')
class API_User(MethodView):

    @bp.response(200, UserDataSchema)
    def get(self, user_id):
        user_data = jsonify(User.query.get_or_404(user_id).to_dict())
        return user_data

    @bp.arguments(UserUpdateSchema)
    @bp.response(200, UserDataSchema)
    def put(self, user_id):
        pass

@bp.response(200, UsersCollectionDataSchema)
@bp.route('/api/users/<int:user_id>/followers', methods=['GET'])
def get_followers(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get(key='page', default=1, type=int)
    per_page = min(request.args.get(key='per_page', default=10, type=int), 100)
    data = User.to_collection_dict(user.followers, page=page, per_page=per_page, endpoint='users.get_followers', user_id=user_id)
    return jsonify(data)

@bp.response(200, UsersCollectionDataSchema)
@bp.route('/api/users/<int:user_id>/followed', methods=['GET'])
def get_followed(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get(key='page', default=1, type=int)
    per_page = min(request.args.get(key='per_page', default=10, type=int), 100)
    data = User.to_collection_dict(user.followed, page=page, per_page=per_page, endpoint='users.get_followed', user_id=user_id)
    return jsonify(data)


@bp.route('/api/users')
class API_Users(MethodView):

    @bp.response(200, UsersCollectionDataSchema)
    def get(self):
        page = request.args.get(key='page', default=1, type=int)
        per_page = min(request.args.get(key='per_page', default=10, type=int), 100)
        users_data = jsonify(User.to_collection_dict(User.query, page=page, per_page=per_page, endpoint='users.API_Users'))
        return users_data