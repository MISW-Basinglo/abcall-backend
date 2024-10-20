from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.common.decorators import handle_exceptions
from src.common.decorators import validate_permissions
from src.common.enums import Permissions
from src.services import get_all_issues

blueprint = Blueprint("issues_management_api", __name__, url_prefix="/issues_management")


@blueprint.route("", methods=["GET"])
@handle_exceptions
@jwt_required()
@validate_permissions([Permissions.VIEW_ISSUE.value])
def get_issues():
    return get_all_issues(), HTTPStatus.OK


@blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, HTTPStatus.OK
