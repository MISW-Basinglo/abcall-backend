from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from src.common.decorators import handle_exceptions
from src.services.user_services import get_products_by_user_service

blueprint = Blueprint("product_api", __name__, url_prefix="/product")


@blueprint.route("/<int:user_id>", methods=["GET"])
@handle_exceptions
@jwt_required()
def get_products(user_id:int):
    response = get_products_by_user_service(user_id)
    return response, HTTPStatus.OK


@blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, HTTPStatus.OK
