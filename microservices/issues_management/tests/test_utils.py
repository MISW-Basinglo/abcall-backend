from unittest.mock import MagicMock

import pytest
from faker import Faker
from src.common.exceptions import CustomException
from src.common.utils import decode_token
from src.common.utils import format_exception_message
from src.common.utils import RequestRaiseForException
from src.models.entities import AuthUser

auth_user = AuthUser
faker = Faker()


def test_format_exception_message_no_detail():
    exception = Exception("Some error occurred")
    result = format_exception_message(exception)
    assert result == "Some error occurred"


def test_format_exception_message_with_detail():
    exception = Exception("ERROR: Something went wrong. DETAIL: Invalid input detected")
    result = format_exception_message(exception)
    assert result == "Invalid input detected"


def test_format_exception_message_with_cause():
    cause_exception = Exception("Root cause")
    exception = Exception("Some error")
    exception.__cause__ = cause_exception
    result = format_exception_message(exception)
    assert result == "Root cause"


def test_raise_for_exception():
    response = RequestRaiseForException(MagicMock(status_code=400, json=MagicMock(return_value={"msg": "Bad request"})))
    with pytest.raises(CustomException) as exec:
        response.raise_for_status()

    assert exec.value.__str__() == "Bad request"


def test_decode_token(mocker):
    user_id = 1
    claims = {"role": "admin", "permissions": ["read", "write"], "email": faker.email()}
    mocker.patch("src.common.utils.get_jwt", return_value=claims)
    result = decode_token(user_id)
    assert isinstance(result, AuthUser)
    assert result.role == claims["role"]
    assert result.permissions == claims["permissions"]
    assert result.email == claims["email"]
