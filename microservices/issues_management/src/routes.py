from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from src.common.decorators import handle_exceptions
from src.services import create_issue_service
from src.services import get_all_issues_service
from src.services import get_issue_service

blueprint = Blueprint("issues_management_api", __name__, url_prefix="/issues_management")


@blueprint.route("", methods=["GET"])
@handle_exceptions
@jwt_required()
# @validate_permissions([Permissions.VIEW_ISSUE.value])
def get_issues():
    return get_all_issues_service(), HTTPStatus.OK


@blueprint.route("/<int:issue_id>", methods=["GET"])
@handle_exceptions
@jwt_required()
def get_issue(issue_id: int):
    return get_issue_service(issue_id), HTTPStatus.OK


@blueprint.route("", methods=["POST"])
@handle_exceptions
@jwt_required()
# @validate_permissions([Permissions.CREATE_ISSUE.value])
def create_issue():
    create_issue_data = request.get_json()
    return create_issue_service(create_issue_data), HTTPStatus.CREATED


@blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, HTTPStatus.OK
