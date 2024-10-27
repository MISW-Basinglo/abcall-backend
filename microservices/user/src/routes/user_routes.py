from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from src.common.decorators import handle_exceptions
from src.services.user_services import create_client_service
from src.services.user_services import get_user_by_field_service
from src.services.user_services import update_user_service

blueprint = Blueprint("user_api", __name__, url_prefix="/user")


@blueprint.route("", methods=["POST"])
@handle_exceptions
@jwt_required()
# @validate_permissions(role=AllowedRoles.ADMIN.value)
def create_client():
    data = request.get_json()
    return create_client_service(data), HTTPStatus.CREATED


@blueprint.route("/<int:user_id>", methods=["PUT", "PATCH"])
@handle_exceptions
@jwt_required()
def update_user(user_id: int):
    data = request.get_json()
    response = update_user_service(user_id, data)
    return response, HTTPStatus.OK


@blueprint.route("", methods=["GET"])
@handle_exceptions
@jwt_required()
def get_user():
    query_params = request.args.to_dict()
    params = [None, None]
    valid_scopes = ["scope", "dni", "id"]
    for key, value in query_params.items():
        if key in valid_scopes:
            if key == "scope" and value == "me":
                params = ["auth_id", get_jwt_identity()]
            else:
                params = [key, value]
            break
    response = get_user_by_field_service(params)
    return response, HTTPStatus.OK


@blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, HTTPStatus.OK
