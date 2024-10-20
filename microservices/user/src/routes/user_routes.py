from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from src.common.decorators import handle_exceptions
from src.common.decorators import validate_permissions
from src.common.enums import AllowedRoles
from src.services.user_services import create_client_service
from src.services.user_services import get_user_session

blueprint = Blueprint("user_api", __name__, url_prefix="/user")


@blueprint.route("", methods=["POST"])
@handle_exceptions
@jwt_required()
@validate_permissions(role=AllowedRoles.ADMIN.value)
def create_client():
    data = request.get_json()
    return create_client_service(data), HTTPStatus.CREATED


@blueprint.route("/me", methods=["GET"])
@handle_exceptions
@jwt_required()
def get_user():
    current_user = get_jwt_identity()
    response = get_user_session(current_user)
    return response, HTTPStatus.OK


@blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, HTTPStatus.OK
