from unittest.mock import MagicMock

import pytest
from faker import Faker
from src.repositories.user_repository import UserRepository

fake = Faker()


def test_get_responsible_by_company(mock_app):
    with mock_app.app_context(), mock_app.test_request_context():
        user_repository = UserRepository()
        email = fake.email()
        user_repository.get_by_query = MagicMock(return_value=[{"auth_id": 1}])
        user_repository.get_auth_user_data_service = MagicMock(return_value={"role": "client", "email": email})
        result = user_repository.get_responsible_by_company(1)
        assert result["email"] == email
        assert result["auth_id"] == 1
        user_repository.get_by_query.assert_called_once()
        user_repository.get_auth_user_data_service.assert_called_once()


def test_get_responsible_by_company_no_responsible(mock_app):
    with mock_app.app_context(), mock_app.test_request_context():
        user_repository = UserRepository()
        user_repository.get_by_query = MagicMock(return_value=[{"auth_id": 1}])
        user_repository.get_auth_user_data_service = MagicMock(return_value={"role": "admin", "email": fake.email()})
        with pytest.raises(Exception) as exec:
            user_repository.get_responsible_by_company(1)
        user_repository.get_by_query.assert_called_once()
        user_repository.get_auth_user_data_service.assert_called_once()
        assert exec.value.__str__() == "No responsible found for company"
