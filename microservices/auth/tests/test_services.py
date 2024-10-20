import pytest
from pytest_mock import mocker  # noqa
from src.common.enums import ExceptionsMessages
from src.common.exceptions import ResourceNotFoundException
from src.common.exceptions import UserNotAuthorizedException
from src.services import authenticate
from src.services import refresh_access_token

from .conftest import login_data
from .conftest import mock_app
from .conftest import mock_user


def test_authenticate_success(mock_app, mock_user, login_data, mocker):
    with mock_app.app_context():
        mock_load_with_exception = mocker.patch("src.serializers.serializers.UserLoginSerializer.load")
        mock_get_user_by_email = mocker.patch("src.repositories.base.BaseRepository.get_by_field")
        mock_generate_token = mocker.patch("src.services.generate_token")
        mock_create_refresh_token = mocker.patch("flask_jwt_extended.create_refresh_token")
        mock_update_auth = mocker.patch("src.repositories.base.BaseRepository.update")
        mock_dump = mocker.patch("src.serializers.serializers.TokenSerializer.dump")
        mock_load_with_exception.return_value = login_data
        mock_get_user_by_email.return_value = mock_user
        mock_generate_token.return_value = "access_token"
        mock_create_refresh_token.return_value = "refresh_token"
        mock_dump.return_value = {"access_token": "access_token", "refresh_token": "refresh_token"}
        result = authenticate(login_data)
        assert result == {
            "access_token": "access_token",
            "refresh_token": "refresh_token",
        }
        mock_load_with_exception.assert_called_once_with(login_data)
        mock_get_user_by_email.assert_called_once_with("email", login_data["email"])
        mock_user.check_password.assert_called_once_with(login_data["password"])
        mock_generate_token.assert_called_once_with(mock_user)
        mock_update_auth.assert_called_once_with(mock_user.id, {"last_login": mocker.ANY})
        mock_dump.assert_called_once()


def test_authenticate_user_not_registered(mock_app, login_data, mocker):
    with mock_app.app_context():
        mock_load_with_exception = mocker.patch("src.serializers.serializers.UserLoginSerializer.load")
        mock_get_user_by_email = mocker.patch("src.repositories.base.BaseRepository.get_by_field")
        mock_load_with_exception.return_value = login_data
        mock_get_user_by_email.return_value = None

        with pytest.raises(ResourceNotFoundException) as excinfo:
            authenticate(login_data)

        assert str(excinfo.value) == ExceptionsMessages.USER_NOT_REGISTERED.value


def test_authenticate_invalid_password(mock_app, mock_user, login_data, mocker):
    with mock_app.app_context():
        mock_load_with_exception = mocker.patch("src.serializers.serializers.UserLoginSerializer.load")
        mock_get_user_by_email = mocker.patch("src.repositories.base.BaseRepository.get_by_field")
        mock_load_with_exception.return_value = login_data
        mock_user.check_password.return_value = False  # Simulate incorrect password
        mock_get_user_by_email.return_value = mock_user
        with pytest.raises(UserNotAuthorizedException) as excinfo:
            authenticate(login_data)

        assert str(excinfo.value) == ExceptionsMessages.INVALID_PASSWORD.value


def test_refresh_access_token_success(mock_app, mock_user, login_data, mocker):
    with mock_app.app_context():
        mock_get_user_by_id = mocker.patch("src.repositories.base.BaseRepository.get_by_field")
        mock_generate_token = mocker.patch("src.services.generate_token")
        mock_user.id = 1
        mock_get_user_by_id.return_value = mock_user
        mock_generate_token.return_value = "new_access_token"
        result = refresh_access_token(1)
        assert result == {"access_token": "new_access_token"}
        mock_get_user_by_id.assert_called_once_with("id", 1)
        mock_generate_token.assert_called_once_with(mock_user)


def test_refresh_access_token_user_not_registered(mock_app, mocker):
    with mock_app.app_context():
        mock_get_user_by_id = mocker.patch("src.repositories.base.BaseRepository.get_by_field")
        mock_get_user_by_id.return_value = None
        with pytest.raises(UserNotAuthorizedException) as excinfo:
            refresh_access_token(0)
        assert str(excinfo.value) == ExceptionsMessages.USER_NOT_REGISTERED.value
