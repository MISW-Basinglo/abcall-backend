from faker import Faker
from pytest_mock import mocker  # noqa
from src.services.company_services import create_company_service
from src.services.company_services import get_all_companies
from src.services.company_services import get_company_by_id
from src.services.company_services import get_company_by_user_session
from tests.conftest import mock_app
from tests.conftest import session

fake = Faker()


# Test para get_all_companies
def test_get_all_companies(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        # Datos simulados
        companies = []
        for i in range(10):
            company_data = {
                "id": i,
                "name": fake.company(),
                "nit": fake.ean(length=13),
                "plan": "Emprendedor",
                "status": "active",
                "created_at": fake.date_time(),
                "updated_at": fake.date_time(),
            }
            companies.append(company_data)

        # Mockeamos el repositorio
        mock_repo = mocker.patch("src.repositories.company_repository.CompanyRepository.get_all", return_value=companies)

        all_companies = get_all_companies()["data"]

        assert len(all_companies) == len(companies)
        mock_repo.assert_called_once()

    for expected, fetched in zip(companies, all_companies):
        assert expected["name"] == fetched["name"]
        assert expected["nit"] == fetched["nit"]
        assert expected["plan"] == fetched["plan"]


# Test para insert_company
def test_insert_company(mock_app, mocker, session):
    with mock_app.app_context(), mock_app.test_request_context():
        mocker.patch("src.db.SessionLocal", return_value=session)
        company_data = {
            "name": fake.company(),
            "nit": fake.ean(length=13),
            "plan": "basic",
            "status": "active",
        }
        return_value = {
            "id": 1,
            "name": company_data["name"],
            "nit": company_data["nit"],
            "plan": company_data["plan"],
            "status": company_data["status"],
            "created_at": fake.date_time(),
            "updated_at": fake.date_time(),
        }
        mocker.patch("src.repositories.company_repository.CompanyRepository.create", return_value=return_value)

        response = create_company_service(company_data)
        assert response["data"]["name"] == company_data["name"]
        assert response["data"]["nit"] == company_data["nit"]
        assert response["data"]["plan"] == company_data["plan"]
        assert response["data"]["id"]


# Test para get_company_by_id
def test_get_company_by_id(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        company_data = {
            "id": 1,
            "name": fake.company(),
            "nit": fake.ean(length=13),
            "plan": "premium",
            "status": "active",
        }
        user_data = {"email": fake.email(), "role": "client"}
        users = [
            {
                "id": 1,
                "name": fake.name(),
                "auth_id": 123,
                "company_id": 1,
                "phone": fake.phone_number(),
                "dni": fake.ean(length=13),
            },
        ]
        mock_repo = mocker.patch("src.repositories.company_repository.CompanyRepository.get_by_field", return_value=company_data)
        mocker.patch("src.repositories.user_repository.UserRepository.get_auth_user_data_service", return_value=user_data)
        mocker.patch("src.repositories.user_repository.UserRepository.get_by_query", return_value=users)
        company = get_company_by_id(1)["data"]

        assert company["name"] == company_data["name"]
        assert company["nit"] == company_data["nit"]
        assert company["plan"] == company_data["plan"]
        mock_repo.assert_called_once_with("id", 1)


# Test para get_company_by_user_session
def test_get_company_by_user_session(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        user_data = {
            "id": 1,
            "name": fake.name(),
            "auth_id": 123,
            "company_id": 1,
        }
        company_data = {
            "id": 1,
            "name": fake.company(),
            "nit": fake.ean(length=13),
            "plan": "basic",
            "status": "active",
        }
        mock_user_repo = mocker.patch("src.repositories.user_repository.UserRepository.get_by_field", return_value=user_data)
        mock_company_repo = mocker.patch("src.repositories.company_repository.CompanyRepository.get_by_field", return_value=company_data)

        company = get_company_by_user_session(123)["data"]

        assert company["name"] == company_data["name"]
        assert company["nit"] == company_data["nit"]
        assert company["plan"] == company_data["plan"]
        mock_user_repo.assert_called_once_with("auth_id", 123)
        mock_company_repo.assert_called_once_with("id", user_data["company_id"])
