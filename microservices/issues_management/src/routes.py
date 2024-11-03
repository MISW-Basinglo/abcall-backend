import base64
import json
from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from src.common.decorators import handle_exceptions
from src.common.enums import ExceptionsMessages
from src.common.exceptions import InvalidParameterException
from src.common.logger import logger
from src.services import create_issue_service
from src.services import create_issue_webhook_service
from src.services import get_all_issues_service
from src.services import get_issue_call_service
from src.services import get_issue_open_service
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


@blueprint.route("/open/<int:user_id>", methods=["GET"])
@handle_exceptions
@jwt_required()
def get_issue_open_by_user(user_id: int):
    return get_issue_open_service(user_id), HTTPStatus.OK


@blueprint.route("/call/<int:user_id>", methods=["GET"])
@handle_exceptions
@jwt_required()
def get_issue_call_by_user(user_id: int):
    return get_issue_call_service(user_id), HTTPStatus.OK


@blueprint.route("", methods=["POST"])
@handle_exceptions
@jwt_required()
# @validate_permissions([Permissions.CREATE_ISSUE.value])
def create_issue():
    create_issue_data = request.get_json()
    return create_issue_service(create_issue_data), HTTPStatus.CREATED


@blueprint.route("/webhook", methods=["POST"])
@handle_exceptions
def create_issue_webhook():
    try:
        envelope = request.get_json()
        pubsub_message = envelope.get("message", {})
        message_data = pubsub_message.get("data")

        if not (envelope and pubsub_message and message_data):
            raise InvalidParameterException(ExceptionsMessages.INVALID_PARAMETER.value)

        decoded_data = base64.b64decode(message_data).decode("utf-8")
        issue_data = json.loads(decoded_data)

        logger.info("Issue data successfully decoded and parsed.")

    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding failed: {e}")
        raise InvalidParameterException("Invalid JSON data.")
    except KeyError as e:
        logger.error(f"Missing key in request: {e}")
        raise InvalidParameterException("Missing required data.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise InvalidParameterException(ExceptionsMessages.INVALID_PARAMETER.value)

    return create_issue_webhook_service(issue_data), HTTPStatus.CREATED


@blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, HTTPStatus.OK
