from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from src.common.decorators import handle_exceptions
from src.services import get_company_by_id, get_all_companies, insert_company, get_company_by_user_session

blueprint = Blueprint("company_api", __name__, url_prefix="/company")

@blueprint.route("/", methods=["POST"])
@handle_exceptions
@jwt_required()
def add_company():
    data = request.get_json()
    return insert_company(data), HTTPStatus.CREATED


@blueprint.route("/<int:id>", methods=["GET"])
@handle_exceptions
@jwt_required()
def get_company(id):
    response = get_company_by_id(id)
    return response, HTTPStatus.OK

@blueprint.route("", methods=["GET"])
@handle_exceptions
@jwt_required()
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

@blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, HTTPStatus.OK
