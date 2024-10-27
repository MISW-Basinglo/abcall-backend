from random import choice
from random import randint

import pytest
from faker import Faker
from pytest_mock import mocker  # noqa
from src.common.enums import CompanyPlan
from src.common.enums import ExceptionsMessages
from src.common.exceptions import ResourceNotFoundException
from src.services.user_services import create_client_service
from src.services.user_services import create_user_service
from src.services.user_services import delete_user_service
from src.services.user_services import get_user_by_field_service
from src.services.user_services import update_user_service
from tests.conftest import session

fake = Faker()


def test_get_user_session_success(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        # Datos simulados de usuario
        user_data = {
            "id": 1,
            "name": fake.name(),
            "auth_id": 123,
            "company_id": 1,
            "phone": fake.phone_number(),
            "dni": 123456789,
        }

        auth_data = {
            "id": 123,
            "email": fake.email(),
            "role": "admin",
            "status": "ACTIVE",
        }

        # Mock del repositorio de usuarios
        mock_user_repo = mocker.patch("src.repositories.user_repository.UserRepository.get_by_field", return_value=user_data)
        mock_user_data = mocker.patch("src.repositories.user_repository.UserRepository.get_auth_user_data_service", return_value=auth_data)

        # Llamada al servicio para obtener la sesión de usuario
        response = get_user_by_field_service(["dni", 123456789])["data"]
        # Aserciones para validar los datos retornados
        assert response["id"] == user_data["id"]
        assert response["name"] == user_data["name"]

        # Verificar que el método del repositorio fue llamado correctamente
        mock_user_repo.assert_called_once_with("dni", 123456789)
        mock_user_data.assert_called_once_with(123)


def test_get_user_session_not_found(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        # Mock para cuando no se encuentra el usuario
        mock_user_repo = mocker.patch(
            "src.repositories.user_repository.UserRepository.get_by_field",
            side_effect=ResourceNotFoundException(ExceptionsMessages.RESOURCE_NOT_FOUND.value),
        )

        # Verificamos que la excepción se lanza cuando no se encuentra el usuario
        with pytest.raises(ResourceNotFoundException) as exc_info:
            get_user_by_field_service(["auth_id", 123])

        # Validamos el mensaje de la excepción
        assert str(exc_info.value) == ExceptionsMessages.RESOURCE_NOT_FOUND.value

        # Verificar que el método del repositorio fue llamado correctamente
        mock_user_repo.assert_called_once_with("auth_id", 123)


def test_create_client(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        fake_client_data = {
            "company_name": fake.company(),
            "nit": f"{randint(1000000, 9999999)}-{randint(1, 9)}",
            "plan": choice([plan.value for plan in CompanyPlan]),
            "user_name": fake.name(),
            "phone": fake.phone_number(),
            "email": fake.email(),
        }
        mocker.patch("src.services.user_services.send_request", return_value={"data": {"id": 1}})
        result = create_client_service(fake_client_data)

        assert result["data"]["company_name"] == fake_client_data["company_name"]
        assert result["data"]["nit"] == fake_client_data["nit"]
        assert result["data"]["plan"] == fake_client_data["plan"]
        assert result["data"]["user_name"] == fake_client_data["user_name"]
        assert result["data"]["phone"] == fake_client_data["phone"]
        assert result["data"]["email"] == fake_client_data["email"]


def test_create_cliente_exception_raised_when_serializing_response(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        fake_client_data = {
            "company_name": fake.company(),
            "nit": f"{randint(1000000, 9999999)}-{randint(1, 9)}",
            "plan": choice([plan.value for plan in CompanyPlan]),
            "user_name": fake.name(),
            "phone": fake.phone_number(),
            "email": fake.email(),
        }
        mocker.patch("src.services.user_services.send_request", return_value={"data": {"id": 1}})
        mocker.patch("src.services.user_services.GenericResponseSerializer.dump", side_effect=Exception)
        with pytest.raises(Exception):
            create_client_service(fake_client_data)


def test_create_user_service(mock_app, session):
    with mock_app.app_context(), mock_app.test_request_context():
        user_data = {"name": fake.name(), "company_id": 1, "phone": fake.phone_number(), "auth_id": 1}
        user = create_user_service(user_data)
        assert user["name"] == user_data["name"]
        assert user["company_id"] == user_data["company_id"]
        assert user["phone"] == user_data["phone"]
        assert user["auth_id"] == user_data["auth_id"]


def test_update_user_service(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        user_data = {"name": fake.name(), "phone": fake.phone_number(), "channel": "SMS", "email": fake.email()}
        mocker.patch("src.repositories.user_repository.UserRepository.update", return_value=user_data)
        mocker.patch("src.services.user_services.get_jwt_identity", return_value=1)
        mocker.patch("src.services.user_services.update_auth_user_service", return_value={"data": user_data})
        response = update_user_service(1, user_data)["data"]
        assert response["name"] == user_data["name"]
        assert response["phone"] == user_data["phone"]
        assert response["channel"] == user_data["channel"]


def test_delete_user_service(mock_app, session):
    with mock_app.app_context(), mock_app.test_request_context():
        user_data = {"name": fake.name(), "company_id": 1, "phone": fake.phone_number(), "auth_id": 1}
        user = create_user_service(user_data)
        assert user["name"] == user_data["name"]
        assert user["company_id"] == user_data["company_id"]
        assert user["phone"] == user_data["phone"]
        assert user["auth_id"] == user_data["auth_id"]
        delete_user_service(user["id"])
        with pytest.raises(ResourceNotFoundException) as exc_info:
            get_user_by_field_service(["id", user["id"]])
        assert str(exc_info.value) == ExceptionsMessages.RESOURCE_NOT_FOUND.value
