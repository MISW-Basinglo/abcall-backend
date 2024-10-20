import pytest
from faker import Faker
from pytest_mock import mocker  # noqa
from src.common.enums import ExceptionsMessages
from src.common.exceptions import ResourceNotFoundException
from src.services.user_services import get_user_session

fake = Faker()


def test_get_user_session_success(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        # Datos simulados de usuario
        user_data = {
            "id": 1,
            "name": fake.name(),
            "auth_id": 123,
            "company_id": 1,
        }

        # Mock del repositorio de usuarios
        mock_user_repo = mocker.patch("src.repositories.user_repository.UserRepository.get_by_field", return_value=user_data)

        # Llamada al servicio para obtener la sesión de usuario
        response = get_user_session(123)["data"]

        # Aserciones para validar los datos retornados
        assert response["id"] == user_data["id"]
        assert response["auth_id"] == user_data["auth_id"]
        assert response["name"] == user_data["name"]

        # Verificar que el método del repositorio fue llamado correctamente
        mock_user_repo.assert_called_once_with("auth_id", 123)


def test_get_user_session_not_found(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        # Mock para cuando no se encuentra el usuario
        mock_user_repo = mocker.patch("src.repositories.user_repository.UserRepository.get_by_field", return_value=None)

        # Verificamos que la excepción se lanza cuando no se encuentra el usuario
        with pytest.raises(ResourceNotFoundException) as exc_info:
            get_user_session(123)

        # Validamos el mensaje de la excepción
        assert str(exc_info.value) == ExceptionsMessages.USER_NOT_REGISTERED.value

        # Verificar que el método del repositorio fue llamado correctamente
        mock_user_repo.assert_called_once_with("auth_id", 123)
