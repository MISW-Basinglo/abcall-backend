from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from src.common.decorators import handle_exceptions
from src.services.services import get_generative_data
from src.services.services import get_predictive_data

blueprint = Blueprint("auth_api", __name__, url_prefix="/ai")


@blueprint.route("/generative", methods=["POST"])
@handle_exceptions
@jwt_required()
def generative():
    data = request.get_json()
    return get_generative_data(data), HTTPStatus.OK


@blueprint.route("/predictive", methods=["POST"])
@handle_exceptions
@jwt_required()
def predictive():
    data = request.get_json()
    return get_predictive_data(data), HTTPStatus.OK


@blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, HTTPStatus.OK
