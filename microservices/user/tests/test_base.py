from unittest.mock import MagicMock

import pytest
from src.common.enums import ExceptionsMessages
from src.common.exceptions import InvalidParameterException
from src.common.exceptions import ResourceNotFoundException
from src.repositories.base import BaseRepository


class TestModel:
    id = 1
    name = "Test Name"
    status = "active"


@pytest.fixture
def repository():
    class TestRepository(BaseRepository):
        model = TestModel

    return TestRepository()


def test_get_by_field_invalid_field(repository, mocker):
    mock_session = MagicMock()
    mocker.patch("src.db.SessionLocal", return_value=mock_session)
    mock_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(InvalidParameterException) as exc_info:
        repository.get_by_field("invalid_field", "Test Name")
    assert str(exc_info.value) == ExceptionsMessages.INVALID_PARAMETER.value


def test_update_not_found(repository, mocker):
    mock_session = MagicMock()
    mocker.patch("src.db.SessionLocal", return_value=mock_session)
    mocker.patch.object(repository, "_get_by_field", return_value=None)

    with pytest.raises(ResourceNotFoundException):
        repository.update(1, {"name": "Updated Test"})


def test_delete_not_found(repository, mocker):
    mock_session = MagicMock()
    mocker.patch("src.db.SessionLocal", return_value=mock_session)
    mocker.patch.object(repository, "_get_by_field", return_value=None)

    with pytest.raises(ResourceNotFoundException):
        repository.delete(1)


def test_create(repository, mocker):
    mock_session = MagicMock()
    mocker.patch("src.db.SessionLocal", return_value=mock_session)
    mocker.patch.object(repository, "_create", return_value=TestModel)

    result = repository.create({"name": "Test Name", "status": "active"})
    assert result == TestModel


def test_get_all(repository, mocker):
    mock_session = MagicMock()
    mocker.patch("src.db.SessionLocal", return_value=mock_session)
    mocker.patch.object(repository, "_get_all", return_value=[TestModel])

    result = repository.get_all()
    assert result == [TestModel]


def test_update(repository, mocker):
    mock_session = MagicMock()
    mocker.patch("src.db.SessionLocal", return_value=mock_session)
    mocker.patch.object(repository, "_update", return_value=TestModel)

    result = repository.update(1, {"name": "Updated Test"})
    assert result == TestModel
