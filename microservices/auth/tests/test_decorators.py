from http import HTTPStatus

import pytest  # noqa
from src.common.decorators import handle_exceptions
from src.common.enums import ExceptionsMessages
from src.common.exceptions import CustomException
from src.common.exceptions import InvalidParameterException
from src.common.exceptions import ResourceExistsException
from src.common.exceptions import ResourceNotFoundException
from src.common.exceptions import TokenNotFoundException
from src.common.exceptions import UserNotAuthorizedException


def test_handle_resource_not_found_exception():
    @handle_exceptions
    def func():
        raise ResourceNotFoundException(ExceptionsMessages.RESOURCE_NOT_FOUND.value)

    response, status_code = func()
    response_obj = {"status": "error", "msg": ExceptionsMessages.RESOURCE_NOT_FOUND.value}
    assert status_code == HTTPStatus.NOT_FOUND
    assert response == response_obj


def test_handle_invalid_parameter_exception():
    @handle_exceptions
    def func():
        raise InvalidParameterException(ExceptionsMessages.INVALID_PARAMETER.value)

    response, status_code = func()
    response_obj = {"status": "error", "msg": ExceptionsMessages.INVALID_PARAMETER.value}
    assert status_code == HTTPStatus.BAD_REQUEST
    assert response == response_obj


def test_handle_user_not_authorized_exception():
    @handle_exceptions
    def func():
        raise UserNotAuthorizedException(ExceptionsMessages.USER_NOT_AUTHORIZED.value)

    response, status_code = func()
    response_obj = {"status": "error", "msg": ExceptionsMessages.USER_NOT_AUTHORIZED.value}
    assert status_code == HTTPStatus.UNAUTHORIZED
    assert response == response_obj


def test_handle_resource_exists_exception():
    @handle_exceptions
    def func():
        raise ResourceExistsException(ExceptionsMessages.RESOURCE_EXISTS.value)

    response, status_code = func()
    response_obj = {"status": "error", "msg": ExceptionsMessages.RESOURCE_EXISTS.value}
    assert status_code == HTTPStatus.CONFLICT
    assert response == response_obj


def test_handle_token_not_found_exception():
    @handle_exceptions
    def func():
        raise TokenNotFoundException(ExceptionsMessages.TOKEN_NOT_FOUND.value)

    response, status_code = func()
    response_obj = {"status": "error", "msg": ExceptionsMessages.TOKEN_NOT_FOUND.value}
    assert status_code == HTTPStatus.FORBIDDEN
    assert response == response_obj


def test_handle_custom_exception():
    @handle_exceptions
    def func():
        raise CustomException("Custom error", status_code=HTTPStatus.PAYMENT_REQUIRED)

    response, status_code = func()
    response_obj = {"status": "error", "msg": "Custom error"}
    assert status_code == HTTPStatus.PAYMENT_REQUIRED
    assert response == response_obj


def test_handle_generic_exception():
    @handle_exceptions
    def func():
        raise ValueError(ExceptionsMessages.ERROR.value)

    response, status_code = func()
    response_obj = {"status": "error", "msg": ExceptionsMessages.ERROR.value}
    assert status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response == response_obj
