from flask import jsonify
from app import db
from flask.views import MethodView
from flask_smorest import Blueprint
from app.api.v1.auth import basic_auth, token_auth


bp = Blueprint(name="tokens", import_name=__name__, description="Operations for tokens")


@bp.route("/api/v1/tokens")
class Token(MethodView):
    @basic_auth.login_required
    def post(self):
        token = basic_auth.current_user().get_token()
        db.session.commit()
        return jsonify({"token": token})

    @bp.response(204)
    @token_auth.login_required
    def delete(self):
        token_auth.current_user().revoke_token()
        db.session.commit()
