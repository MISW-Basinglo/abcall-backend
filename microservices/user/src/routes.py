from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from src.common.decorators import handle_exceptions
from src.services import get_company_by_id, get_all_companies, insert_company, get_company_by_user_session

blueprint = Blueprint("user_api", __name__, url_prefix="/user")


@blueprint.route("/company", methods=["POST"])
@handle_exceptions
@jwt_required()
def addCompany():
    data = request.get_json()
    return insert_company(data), HTTPStatus.CREATED


@blueprint.route("/company/<int:id>", methods=["GET"])
@handle_exceptions
@jwt_required()
def getCompany(id):
    response = get_company_by_id(id)
    return response, HTTPStatus.OK

@blueprint.route("/company", methods=["GET"])
@handle_exceptions
@jwt_required()
def getCompanies():
    response = get_all_companies()
    return response, HTTPStatus.OK

@blueprint.route("/company/client", methods=["GET"])
@handle_exceptions
@jwt_required()
def refresh():
    current_user = get_jwt_identity()
    response = get_company_by_user_session(current_user)
    return response, HTTPStatus.OK

@blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, HTTPStatus.OK
