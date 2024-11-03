from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from src.common.decorators import handle_exceptions
from src.services.company_services import create_company_service
from src.services.company_services import get_all_companies
from src.services.company_services import get_company_by_id
from src.services.company_services import get_company_by_user_session
from src.services.company_services import update_company_service
from src.services.company_services import get_users_by_company_session

blueprint = Blueprint("company_api", __name__, url_prefix="/company")


@blueprint.route("/", methods=["POST"])
@handle_exceptions
@jwt_required()
def add_company():
    data = request.get_json()
    return create_company_service(data), HTTPStatus.CREATED


@blueprint.route("/<int:company_id>", methods=["GET"])
@handle_exceptions
@jwt_required()
def get_company(company_id):
    response = get_company_by_id(company_id)
    return response, HTTPStatus.OK


@blueprint.route("", methods=["GET"])
@handle_exceptions
@jwt_required()
# @validate_permissions(role=[AllowedRoles.CLIENT.value, AllowedRoles.ADMIN.value])
def get_companies():
    response = get_all_companies()
    return response, HTTPStatus.OK


@blueprint.route("/client", methods=["GET"])
@handle_exceptions
@jwt_required()
def get_company_user_session():
    current_user = get_jwt_identity()
    response = get_company_by_user_session(current_user)
    return response, HTTPStatus.OK

@blueprint.route("/users", methods=["GET"])
@handle_exceptions
@jwt_required()
def get_users_company_session():
    current_user = get_jwt_identity()
    response = get_users_by_company_session(current_user)
    return response, HTTPStatus.OK


@blueprint.route("/<int:company_id>", methods=["PUT", "PATCH"])
@handle_exceptions
@jwt_required()
# @validate_permissions(role=AllowedRoles.ADMIN.value)
def update_company(company_id: int):
    data = request.get_json()
    response = update_company_service(company_id, data)
    return response, HTTPStatus.OK


@blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, HTTPStatus.OK
