from datetime import datetime
from datetime import timedelta

import requests
from src.common.constants import BACKEND_HOST
from src.common.constants import DAEMON_REQUEST_HEADER_VALUE
from src.common.constants import MAIL_GAP
from src.models.entities import AuthUser
from src.models.entities import User


read_emails = set()


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


def is_message_sent(mail_id):
    is_sent = any(msg_id == mail_id for msg_id, _ in read_emails)
    return is_sent


def add_email_to_sent_list(mail_id):
    current_time = datetime.now()
    expiration_time = timedelta(seconds=MAIL_GAP)
    # Remove expired emails
    read_emails.difference_update({(msg_id, timestamp) for msg_id, timestamp in read_emails if current_time - timestamp > expiration_time})
    # Add new email
    read_emails.add((mail_id, current_time))
