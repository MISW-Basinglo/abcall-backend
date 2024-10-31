from unittest.mock import Mock

from pytest_mock import mocker  # noqa
from src.common.constants import BACKEND_HOST
from src.common.utils import get_auth_user_data
from src.common.utils import get_url
from src.common.utils import get_user_data
from src.common.utils import send_request
from src.models.entities import AuthUser
from src.models.entities import User


def test_get_url():
    auth_url = get_url("auth", params={"email": "test@example.com"})
    assert auth_url == f"{BACKEND_HOST}/auth/email?email=test@example.com"

    user_url = get_url("user", identifier=1)
    assert user_url == f"{BACKEND_HOST}/user/1"

    unknown_url = get_url("unknown")
    assert unknown_url == BACKEND_HOST


def test_send_request(mocker):
    response = Mock()
    response.json.return_value = {"data": "test"}
    response.raise_for_status.return_value = None

    mocker.patch("src.common.utils.requests.request", return_value=response)

    result = send_request("GET", "http://test.com")
    assert result == {"data": "test"}


def test_get_user_data(mocker):
    user_data = {"id": 1, "company_id": 1, "auth_id": 1, "name": "test", "phone": "1234567890"}

    mocker.patch("src.common.utils.send_request", return_value={"data": user_data})

    result = get_user_data(1)
    assert isinstance(result, User)
    assert result.id == 1
    assert result.company_id == 1
    assert result.auth_id == 1
    assert result.name == "test"
    assert result.phone == "1234567890"


def test_get_auth_user_data(mocker):
    user_data = {
        "id": 1,
        "email": "test@example.com",
        "status": "ACTIVE",
        "role": "admin",
    }
    mocker.patch("src.common.utils.get_url", return_value="http://test.com")
    mocker.patch("src.common.utils.send_request", return_value={"data": user_data})
    result = get_auth_user_data("test@example.com")
    assert isinstance(result, AuthUser)
    assert result.id == 1
    assert result.role == "admin"
    assert result.status == "ACTIVE"
