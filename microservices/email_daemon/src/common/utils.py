import requests
from src.common.constants import BACKEND_HOST
from src.common.constants import DAEMON_REQUEST_HEADER_VALUE
from src.models.entities import AuthUser
from src.models.entities import User


def get_auth_user_data(from_address) -> AuthUser:
    url = get_url("auth", {"email": from_address})
    user_data = send_request("GET", url)["data"]
    return AuthUser(**user_data)


def get_user_data(user_id) -> User:
    url = get_url("user", identifier=user_id)
    user_data = send_request("GET", url)["data"]
    return User(**user_data)


def send_request(method, url, data=None) -> dict:
    headers = {"Content-Type": "application/json", "X-Request-From": DAEMON_REQUEST_HEADER_VALUE}
    response = requests.request(method, url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()


def get_url(path_name, params=None, identifier=None) -> str:
    path_switch = {
        "auth": "/auth/email",
        "user": "/user",
    }
    base = BACKEND_HOST
    url = base + path_switch.get(path_name, "")
    if params:
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
    if identifier:
        url += f"/{identifier}"
    return url
