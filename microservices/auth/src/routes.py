from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask import Response
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from src.common.decorators import handle_exceptions
from src.services import audit_decode_token
from src.services import authenticate
from src.services import create_user_auth
from src.services import delete_auth_user_service
from src.services import get_auth_user_by_field_service
from src.services import refresh_access_token
from src.services import update_user_auth

blueprint = Blueprint("auth_api", __name__, url_prefix="/auth")


@blueprint.route("", methods=["POST"])
@handle_exceptions
@jwt_required()
def register():
    data = request.get_json()
    return create_user_auth(data), HTTPStatus.CREATED


@blueprint.route("/<int:auth_id>", methods=["DELETE"])
@handle_exceptions
@jwt_required()
def delete(auth_id: int):
    delete_auth_user_service(auth_id)
    return Response(status=HTTPStatus.NO_CONTENT)


@blueprint.route("/<int:auth_id>", methods=["GET"])
@handle_exceptions
@jwt_required()
def get(auth_id: int):
    return get_auth_user_by_field_service(["id", auth_id]), HTTPStatus.OK


@blueprint.route("/<int:auth_id>", methods=["PUT", "PATCH"])
@handle_exceptions
@jwt_required()
def update(auth_id: int):
    data = request.get_json()
    return update_user_auth(auth_id, data), HTTPStatus.OK


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
