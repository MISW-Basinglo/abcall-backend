from unittest.mock import MagicMock
from unittest.mock import Mock

import pytest
from faker import Faker
from src.common.enums import ExceptionsMessages
from src.common.exceptions import CustomException
from src.common.exceptions import InvalidParameterException
from src.common.exceptions import ResourceNotFoundException
from src.repositories.auth_repository import UserAuthRepository
from src.serializers.serializers import UserCreateSerializer
from src.serializers.serializers import UserRetrieveSerializer
from tests.conftest import mock_app
from tests.conftest import session

faker = Faker()


def test_get_by_field_success(mock_app, mock_repository, mocker):
    with mock_app.app_context():
        mocker.patch("src.repositories.base.BaseRepository._get_by_field", return_value=MagicMock())
        field_name = "id"
        field_value = 1
        result = mock_repository.get_by_field(field_name, field_value)
        assert result


def test_get_by_field_attribute_error(mock_app, mock_repository, mocker):
    with mock_app.app_context():
        field_name = "non_existing_field"
        field_value = 1

        mocker.patch.object(mock_repository, "_get_by_field", side_effect=InvalidParameterException(ExceptionsMessages.INVALID_PARAMETER.value))

        with pytest.raises(InvalidParameterException) as exc_info:
            mock_repository.get_by_field(field_name, field_value)

        assert str(exc_info.value) == ExceptionsMessages.INVALID_PARAMETER.value


def test_get_by_field_not_found(mock_app, mock_repository, mocker):
    with mock_app.app_context():
        mocker.patch.object(mock_repository, "_get_by_field", side_effect=ResourceNotFoundException(ExceptionsMessages.RESOURCE_NOT_FOUND.value))
        field_name = "id"
        field_value = 1
        with pytest.raises(ResourceNotFoundException) as exc_info:
            mock_repository.get_by_field(field_name, field_value)
        assert str(exc_info.value) == ExceptionsMessages.RESOURCE_NOT_FOUND.value


def test_update_success(mock_app, session, mocker):
    with mock_app.app_context():
        mocker.patch("src.serializers.serializers.UserRetrieveSerializer.get_role", return_value="admin")
        mocker.patch("src.repositories.auth_repository.UserAuthRepository.get_role", return_value=1)
        serializer_class = UserRetrieveSerializer
        auth_repository = UserAuthRepository()
        auth_repository.set_serializer(serializer_class)

        test_data = {
            "email": faker.email(),
            "password": faker.password(),
            "role": "admin",
        }

        instance = auth_repository.create(test_data)

        assert instance["id"] is not None
        assert instance["email"] == test_data["email"]

        new_data = {
            "email": faker.email(),
        }

        updated_instance = auth_repository.update(instance["id"], new_data)

        assert updated_instance["email"] == new_data["email"]
        assert updated_instance["email"] != test_data["email"]


def test_update_instance_not_found(mock_app, mock_repository, mocker):
    with mock_app.app_context():
        mocker.patch("src.repositories.base.BaseRepository._get_by_field", return_value=None)
        instance_id = 1
        data = {"field": "value"}
        with pytest.raises(ResourceNotFoundException) as exc_info:
            mock_repository.update(instance_id, data)
        assert exc_info.value.__str__() == ExceptionsMessages.RESOURCE_NOT_FOUND.value


def test_update_transaction_failure(mock_app, mock_repository, mocker):
    with mock_app.app_context():
        mocker.patch("src.repositories.base.BaseRepository._update", side_effect=CustomException("Some error"))
        instance_id = 1
        data = {"field": "value"}
        with pytest.raises(CustomException) as exc_info:
            mock_repository.update(instance_id, data)
        assert exc_info.value.__str__() == "Some error"


def test_create_success(mock_app, mocker, session):
    with mock_app.app_context():
        mocker.patch("src.serializers.serializers.UserRetrieveSerializer.get_role", return_value="admin")
        mocker.patch("src.repositories.auth_repository.UserAuthRepository.get_role", return_value=1)
        serializer_class = UserRetrieveSerializer
        auth_repository = UserAuthRepository()
        auth_repository.set_serializer(serializer_class)

        test_data = {
            "email": faker.email(),
            "password": faker.password(),
            "role": "admin",
        }

        instance = auth_repository.create(test_data)

        assert instance["id"] is not None
        assert instance["email"] == test_data["email"]


def test_create_transaction_failure(mock_app, mock_repository, mocker):
    with mock_app.app_context():
        mocker.patch("src.repositories.base.BaseRepository._create", side_effect=CustomException("Some error"))
        data = {"field": "value"}
        with pytest.raises(CustomException) as exc_info:
            mock_repository.create(data)
        assert str(exc_info.value) == "Some error"


def test_delete_instance_not_found(mock_app, mock_repository, mocker):
    with mock_app.app_context():
        mocker.patch("src.repositories.base.BaseRepository._get_by_field", return_value=None)
        instance_id = 1
        with pytest.raises(ResourceNotFoundException) as exc_info:
            mock_repository.delete(instance_id)
        assert exc_info.value.__str__() == ExceptionsMessages.RESOURCE_NOT_FOUND.value


def test_set_serializer(mock_app, mock_repository):
    with mock_app.app_context():
        serializer = MagicMock()
        mock_repository.set_serializer(serializer)
        assert mock_repository.serializer == serializer


def test_get_serializer(mock_app, mock_repository):
    with mock_app.app_context():
        assert mock_repository.get_serializer() is not None
