import random
from random import choice
from random import randint

from faker import Faker
from pytest_mock import mocker  # noqa
from src.common.enums import IssueSource
from src.common.enums import IssueType
from src.services import create_issue_service
from src.services import create_issue_webhook_service
from src.services import get_all_issues_service
from src.services import get_issue_call_service
from src.services import get_issue_open_service
from src.services import get_issue_service
from src.services import get_user_info
from tests.conftest import mock_app
from tests.conftest import session

fake = Faker()


def test_get_all_issues(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        issues = []
        for i in range(10):
            issue_data = {
                "id": i,
                "description": fake.text(),
                "source": choice([enum.value for enum in IssueSource]),
                "type": choice([enum.value for enum in IssueType]),
                "user_id": randint(1, 100),
                "company_id": randint(1, 100),
                "status": "open",
                "created_at": fake.date_time(),
                "updated_at": fake.date_time(),
                "solution": None,
            }
            issues.append(issue_data)
        mock_repo = mocker.patch("src.repositories.issues_repository.IssuesManagementRepository.get_all", return_value=issues)

        all_issues = get_all_issues_service()["data"]

        assert len(all_issues) == len(issues)
        mock_repo.assert_called_once()

    for expected, fetched in zip(issues, all_issues):
        assert expected["description"] == fetched["description"]
        assert expected["source"] == fetched["source"]
        assert expected["type"] == fetched["type"]


def test_create_issue_service(mock_app, mocker, session):
    with mock_app.app_context(), mock_app.test_request_context():
        mocker.patch("src.db.SessionLocal", return_value=session)
        mocker.patch("src.services.get_user_info", return_value={"id": 1, "name": fake.name(), "company_id": 1})
        issue_data = {
            "description": fake.text(),
            "source": choice([enum.value for enum in IssueSource]),
            "type": choice([enum.value for enum in IssueType]),
        }
        fake_user_data = {
            "id": 1,
            "name": fake.name(),
            "company_id": 1,
            "email": fake.email(),
            "role": "user",
        }
        mocker.patch("src.services.get_user_info", return_value=fake_user_data)
        response = create_issue_service(issue_data)["data"]

        assert response["description"] == issue_data["description"]
        assert response["source"] == issue_data["source"]
        assert response["type"] == issue_data["type"]
        assert response["id"] is not None


def test_create_issue_webhook_service(mock_app, mocker, session):
    with mock_app.app_context(), mock_app.test_request_context():
        mocker.patch("src.db.SessionLocal", return_value=session)
        issue_data = {
            "user_id": randint(1, 100),
            "email": fake.email(),
            "description": fake.text(),
            "type": choice([enum.value for enum in IssueType]),
            "source": "EMAIL",
            "company_id": randint(1, 100),
        }

        response = create_issue_webhook_service(issue_data)["data"]

        assert response["description"] == issue_data["description"]
        assert response["source"] == issue_data["source"]
        assert response["type"] == issue_data["type"]
        assert response["id"] is not None


def test_get_user_info(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        fake_user_data = {
            "data": {
                "id": 1,
                "name": fake.name(),
                "company_id": 1,
                "email": fake.email(),
                "role": "user",
            },
        }
        mocker.patch("src.common.utils.get_auth_header_from_request", return_value={"Authorization": "Bearer token"})
        mocker.patch("src.services.send_request", return_value=fake_user_data)
        user_info = get_user_info("1234567890")
        assert user_info == fake_user_data["data"]


def test_get_issue_open_service(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        user_id = 1
        open_issues = [
            {
                "id": i,
                "description": fake.text(),
                "source": choice([enum.value for enum in IssueSource]),
                "type": choice([enum.value for enum in IssueType]),
                "user_id": user_id,
                "company_id": randint(1, 100),
                "status": "OPEN",
                "created_at": fake.date_time(),
                "updated_at": fake.date_time(),
                "solution": None,
            }
            for i in range(5)
        ]

        mock_repo = mocker.patch("src.repositories.issues_repository.IssuesManagementRepository.get_by_query", return_value=open_issues)

        response = get_issue_open_service(user_id)["data"]

        assert len(response) == len(open_issues)
        mock_repo.assert_called_once_with({"user_id": ("eq", user_id), "status": ("eq", "OPEN")})

        for expected, fetched in zip(open_issues, response):
            assert expected["description"] == fetched["description"]
            assert expected["source"] == fetched["source"]
            assert expected["type"] == fetched["type"]


def test_get_issue_service(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        issue_id = 1
        issue = {
            "id": issue_id,
            "description": fake.text(),
            "source": choice([enum.value for enum in IssueSource]),
            "type": choice([enum.value for enum in IssueType]),
            "user_id": randint(1, 100),
            "company_id": randint(1, 100),
            "status": "OPEN",
            "created_at": fake.date_time(),
            "updated_at": fake.date_time(),
            "solution": None,
        }
        mock_repo = mocker.patch("src.repositories.issues_repository.IssuesManagementRepository.get_by_field", return_value=issue)

        response = get_issue_service(issue_id)["data"]

        assert response["description"] == issue["description"]
        assert response["source"] == issue["source"]
        assert response["type"] == issue["type"]
        mock_repo.assert_called_once_with("id", issue_id)


def test_get_issue_call_service(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        user_id = 1
        call_issues = [
            {
                "id": i,
                "description": fake.text(),
                "source": "CALL",
                "type": choice([enum.value for enum in IssueType]),
                "user_id": user_id,
                "company_id": randint(1, 100),
                "status": "OPEN",
                "created_at": fake.date_time(),
                "updated_at": fake.date_time(),
                "solution": None,
            }
            for i in range(3)
        ]
        mock_repo = mocker.patch("src.repositories.issues_repository.IssuesManagementRepository.get_by_query", return_value=call_issues)

        response = get_issue_call_service(user_id)["data"]

        assert len(response) == len(call_issues)
        mock_repo.assert_called_once_with({"user_id": ("eq", user_id), "source": ("eq", "CALL")})

        for expected, fetched in zip(call_issues, response):
            assert expected["description"] == fetched["description"]
            assert expected["source"] == fetched["source"]
            assert expected["type"] == fetched["type"]
