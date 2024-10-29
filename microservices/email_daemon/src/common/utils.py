import requests
from src.common.constants import BACKEND_HOST
from src.common.constants import DAEMON_REQUEST_HEADER_VALUE
from src.models.entities import AuthUser


def get_user_data(from_address) -> AuthUser:
    url = get_url("auth", {"email": from_address})
    user_data = send_request("GET", url)["data"]
    return AuthUser(**user_data)


def send_request(method, url, data=None) -> dict:
    headers = {"Content-Type": "application/json", "X-Request-From": DAEMON_REQUEST_HEADER_VALUE}
    response = requests.request(method, url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()


def get_url(path_name, params=None) -> str:
    path_switch = {
        "auth": "/auth/email",
    }
    base = BACKEND_HOST
    url = base + path_switch.get(path_name, "")
    if params:
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
    return url
