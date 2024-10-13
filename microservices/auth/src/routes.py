from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from src.common.decorators import handle_exceptions
from src.services import audit_decode_token
from src.services import authenticate
from src.services import refresh_access_token

blueprint = Blueprint("auth_api", __name__, url_prefix="/auth")


@blueprint.route("/login", methods=["POST"])
@handle_exceptions
def login():
    data = request.get_json()
    return authenticate(data), HTTPStatus.OK


@blueprint.route("/refresh-token", methods=["POST"])
@handle_exceptions
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    response = refresh_access_token(current_user)
    return response, HTTPStatus.OK


@blueprint.route("/decode-token", methods=["GET"])
@jwt_required()
def decode_token():
    current_user = get_jwt_identity()
    return audit_decode_token(current_user), HTTPStatus.OK


@blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, HTTPStatus.OK
