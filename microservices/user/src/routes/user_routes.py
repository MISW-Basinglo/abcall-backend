from http import HTTPStatus

import base64
import io
import csv

from flask import Blueprint
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request
from src.common.constants import DAEMON_REQUEST_HEADER_VALUE
from src.common.decorators import handle_exceptions
from src.common.enums import ExceptionsMessages
from src.common.exceptions import UserNotAuthorizedException
from src.services.user_services import create_client_service
from src.services.user_services import get_minimal_user_by_field
from src.services.user_services import get_user_by_field_service
from src.services.user_services import update_user_service
from src.services.user_services import imports_users_service

blueprint = Blueprint("user_api", __name__, url_prefix="/user")


@blueprint.route("", methods=["POST"])
@handle_exceptions
@jwt_required()
# @validate_permissions(role=AllowedRoles.ADMIN.value)
def create_client():
    data = request.get_json()
    return create_client_service(data), HTTPStatus.CREATED


@blueprint.route("/import", methods=["POST"])
@handle_exceptions
@jwt_required()
def import_users_session():
    current_user = get_jwt_identity()

   # Obtener la cadena codificada en Base64
    data = request.json.get("users")
    
    # Decodificar la cadena de Base64
    csv_decoded = base64.b64decode(data).decode('utf-8')
    
    # Convertir la cadena en un archivo CSV
    csv_file = io.StringIO(csv_decoded)
    csv_reader = csv.reader(csv_file)

    response = imports_users_service(current_user, csv_reader)
    return response, HTTPStatus.OK


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


@blueprint.route("/<int:user_id>", methods=["GET"])
@handle_exceptions
def get_minimal_user(user_id: int):
    if request.headers.get("X-Request-From") != DAEMON_REQUEST_HEADER_VALUE:
        raise UserNotAuthorizedException(ExceptionsMessages.USER_NOT_AUTHORIZED.value)
    response = get_minimal_user_by_field(["auth_id", user_id])
    return response, HTTPStatus.OK


@blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, HTTPStatus.OK
