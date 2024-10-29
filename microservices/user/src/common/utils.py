# app/utils.py
from http import HTTPStatus

import requests
from flask import request as flask_request
from flask_jwt_extended import get_jwt
from src.common.constants import BACKEND_HOST
from src.common.constants import DAEMON_REQUEST_HEADER_VALUE
from src.common.enums import ExceptionsMessages
from src.common.exceptions import CustomException
from src.common.logger import logger
from src.models.entities import AuthUser


class RequestRaiseForException:
    def __init__(self, response):
        self.response = response

    def raise_for_status(self):
        if HTTPStatus.BAD_REQUEST <= self.response.status_code < HTTPStatus.INTERNAL_SERVER_ERROR:
            raise CustomException(self.response.json()["msg"], status_code=self.response.status_code)
        elif self.response.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
            raise Exception(ExceptionsMessages.ERROR.value)


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
    email = claims.get("email")
    if not role or not permissions:
        logger.error(ExceptionsMessages.ERROR_DECODING_TOKEN.value)
        raise CustomException(ExceptionsMessages.ERROR_DECODING_TOKEN.value)
    return AuthUser(user_id=user_id, role=role, permissions=permissions, email=email)


def get_auth_header_from_request():
    token = flask_request.headers.get("Authorization", None)
    if token and "Bearer" in token:
        return {"Authorization": token}
    return {}


def get_from_header_request():
    from_header = flask_request.headers.get("X-Request-From")
    if from_header == DAEMON_REQUEST_HEADER_VALUE:
        return {"X-Request-From": from_header}
    return {}


def send_request(method, url, data=None, headers=None):
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    else:
        h.update(get_auth_header_from_request())
        h.update(get_from_header_request())
    response = requests.request(method, url, json=data, headers=h)
    RequestRaiseForException(response).raise_for_status()
    return response.json()


def get_request_url(service: str):
    service_switcher = {
        "auth": "/auth",
    }
    return f"{BACKEND_HOST}{service_switcher.get(service, '')}"
