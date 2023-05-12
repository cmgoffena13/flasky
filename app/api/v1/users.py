from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.api.v1.schemas import UserDataSchema, UserUpdateSchema, UserRegisterSchema, UsersCollectionDataSchema
from app.models import User
from flask import jsonify, request
from app.api.v1.errors import bad_request
from app import db
from app.api.v1.auth import token_auth


bp = Blueprint(name="users", import_name=__name__, description="Operations on Users")

# GET = SELECT
# POST = INSERT
# PUT = UPDATE
# DELETE = DELETE
@bp.route('/api/v1/users/<int:user_id>')
class API_User(MethodView):

    @token_auth.login_required
    @bp.response(200, UserDataSchema)
    def get(self, user_id):
        return jsonify(User.query.get_or_404(user_id).to_dict())

    @token_auth.login_required
    @bp.arguments(UserUpdateSchema)
    @bp.response(200, UserDataSchema)
    def put(self, user_data, user_id):
        user = User.query.get_or_404(user_id)
        if 'username' in user_data and user_data['username'] != User.query.filter_by(username=user_data['username']).first():
            abort(409, message="Please use a different username")
        if 'email' in user_data and user_data['email'] != User.query.filter_by(email=user_data['email']).first():
            abort(409, message="Please use a different email address")
        user.from_dict(data=user_data, new_user=False)
        db.session.commit()
        return jsonify(user.to_dict())

@bp.route('/api/v1/users/register')
class API_UserRegister(MethodView):
    
    @token_auth.login_required
    @bp.arguments(UserRegisterSchema)
    @bp.response(201, UserDataSchema)
    def post(self, user_data):
        if User.query.filter(User.username == user_data['username']).first():
            abort(409, message="A user with that username already exists")
        if User.query.filter(User.email == user_data['email']).first():
            abort(409, message="A user with that email already exists")
        user = User()
        user.from_dict(data=user_data, new_user=True)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict())


@bp.response(200, UsersCollectionDataSchema)
@bp.route('/api/v1/users/<int:user_id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get(key='page', default=1, type=int)
    per_page = min(request.args.get(key='per_page', default=10, type=int), 100)
    data = User.to_collection_dict(user.followers, page=page, per_page=per_page, endpoint='users.get_followers', user_id=user_id)
    return jsonify(data)

@bp.response(200, UsersCollectionDataSchema)
@bp.route('/api/v1/users/<int:user_id>/followed', methods=['GET'])
@token_auth.login_required
def get_followed(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get(key='page', default=1, type=int)
    per_page = min(request.args.get(key='per_page', default=10, type=int), 100)
    data = User.to_collection_dict(user.followed, page=page, per_page=per_page, endpoint='users.get_followed', user_id=user_id)
    return jsonify(data)

@bp.route('/api/v1/users/')
class API_Users(MethodView):

    @token_auth.login_required
    @bp.response(200, UsersCollectionDataSchema)
    def get(self):
        page = request.args.get(key='page', default=1, type=int)
        per_page = min(request.args.get(key='per_page', default=10, type=int), 100)
        users_data = jsonify(User.to_collection_dict(User.query, page=page, per_page=per_page, endpoint='users.API_Users'))
        return users_data