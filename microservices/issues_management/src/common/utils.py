# app/utils.py
import requests
from flask import request as flask_request
from flask_jwt_extended import get_jwt
from src.common.enums import ExceptionsMessages
from src.common.exceptions import CustomException
from src.common.logger import logger
from src.models.entities import AuthUser


def format_exception_message(exception: Exception) -> str:
    cause = str(exception.__cause__) if exception.__cause__ else str(exception)

    if "DETAIL:" in cause:
        detail_message = cause.split("DETAIL:")[-1].strip()
        return detail_message.replace("\n", " ").capitalize()

    return cause


def decode_token(user_id: int) -> AuthUser:
    claims = get_jwt()
    role = claims.get("role")
    permissions = claims.get("permissions")
    if not role or not permissions:
        logger.error(ExceptionsMessages.ERROR_DECODING_TOKEN.value)
        raise CustomException(ExceptionsMessages.ERROR_DECODING_TOKEN.value)
    return AuthUser(user_id=user_id, role=role, permissions=permissions)


def get_auth_header_from_request():
    token = flask_request.headers.get("Authorization", None)
    if token and "Bearer" in token:
        return {"Authorization": token}
    return {}


def send_request(url, method, data=None, headers=None):
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    response = requests.request(method, url, json=data, headers=h)
    response.raise_for_status()
    return response.json()
