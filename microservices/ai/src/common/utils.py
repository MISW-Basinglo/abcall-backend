from http import HTTPStatus

import requests
from flask import request as flask_request
from src.common.constants import BACKEND_HOST
from src.common.enums import ExceptionsMessages
from src.common.exceptions import CustomException


class RequestRaiseForException:
    def __init__(self, response):
        self.response = response

    def raise_for_status(self):
        if HTTPStatus.BAD_REQUEST <= self.response.status_code < HTTPStatus.INTERNAL_SERVER_ERROR:
            raise CustomException(self.response.json()["msg"], status_code=self.response.status_code)
        elif self.response.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
            raise Exception(ExceptionsMessages.ERROR.value)


def get_auth_header_from_request():
    token = flask_request.headers.get("Authorization", None)
    if token and "Bearer" in token:
        return {"Authorization": token}
    return {}


def send_request(method, url, data=None, headers=None):
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    else:
        h.update(get_auth_header_from_request())
    response = requests.request(method, url, json=data, headers=h)
    RequestRaiseForException(response).raise_for_status()
    return response.json()


def get_url(path_name, params=None, identifier=None) -> str:
    path_switch = {
        "issues": "/issues_management",
    }
    base = BACKEND_HOST
    url = base + path_switch.get(path_name, "")
    if params:
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
    if identifier:
        url += f"/{identifier}"
    return url
