from unittest.mock import MagicMock
from unittest.mock import Mock

import pytest
from src.common.enums import ExceptionsMessages
from src.common.exceptions import CustomException
from src.common.exceptions import InvalidParameterException
from src.common.exceptions import ResourceNotFoundException
from src.repositories.issues_repository import IssuesManagementRepository
from src.serializers.serializers import IssueListSerializer
from tests.conftest import mock_app
from tests.conftest import mock_repository
from tests.conftest import session


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


def test_update_success(mock_app, mock_repository, mocker):
    with mock_app.app_context():
        mock_update = mocker.patch("src.repositories.base.BaseRepository._update", return_value="Updated Instance")
        mock_repository.get_serializer().dump.return_value = "Updated Instance"
        instance_id = 1
        data = {"field": "value"}

        result = mock_repository.update(instance_id, data)
        mock_update.assert_called_once_with(instance_id, data)
        assert result == "Updated Instance"


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


def test_create_success(mock_app, mock_repository, mocker):
    with mock_app.app_context():
        mock_create = mocker.patch("src.repositories.base.BaseRepository._create", return_value="New Instance")
        mock_repository.get_serializer().dump.return_value = "New Instance"
        data = {"field": "value"}
        result = mock_repository.create(data)
        mock_create.assert_called_once_with(data)
        assert result == "New Instance"


def test_create_transaction_failure(mock_app, mock_repository, mocker):
    with mock_app.app_context():
        mocker.patch("src.repositories.base.BaseRepository._create", side_effect=CustomException("Some error"))
        data = {"field": "value"}
        with pytest.raises(CustomException) as exc_info:
            mock_repository.create(data)
        assert str(exc_info.value) == "Some error"


def test_delete_success(mock_app, mock_repository, mocker):
    with mock_app.app_context():
        mock_delete = mocker.patch("src.repositories.base.BaseRepository._delete")
        instance_id = 1
        mock_repository._get_by_field = Mock(return_value=Mock())
        mock_repository.delete(instance_id)
        mock_delete.assert_called_once_with(instance_id)


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


def test_get_by_query(mock_app, session):
    with mock_app.app_context():
        issue_repository = IssuesManagementRepository(session=session)
        issue_repository.create({"description": "test", "source": "CHATBOT", "type": "REQUEST", "user_id": 1})
        issue_repository.create({"description": "test 2", "source": "CALL", "type": "REQUEST", "user_id": 1})
        issue_repository.create({"description": "test 3", "source": "EMAIL", "type": "REQUEST", "user_id": 2})
        issue_repository.session.close()

        issue_repository = IssuesManagementRepository(session=session)
        issue_repository.set_serializer(IssueListSerializer)
        filter_dict = {"user_id": ("eq", 1)}
        issues = issue_repository.get_by_query(filter_dict)
        assert len(issues) == 2

        filter_dict = {"user_id": ("eq", 2)}
        issues = issue_repository.get_by_query(filter_dict)
        assert len(issues) == 1
