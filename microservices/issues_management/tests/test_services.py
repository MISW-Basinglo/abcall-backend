from random import choice
from random import randint

from faker import Faker
from pytest_mock import mocker  # noqa
from src.common.enums import IssueSource
from src.common.enums import IssueType
from src.services import create_issue_service
from src.services import get_all_issues_service
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
        return_value = {
            "id": 1,
            "description": issue_data["description"],
            "source": issue_data["source"],
            "type": issue_data["type"],
            "user_id": 1,
            "company_id": 1,
            "status": "open",
            "created_at": fake.date_time(),
            "updated_at": fake.date_time(),
            "solution": None,
        }
        mocker.patch("src.repositories.issues_repository.IssuesManagementRepository.create", return_value=return_value)

        response = create_issue_service(issue_data)
        assert response["data"]["description"] == issue_data["description"]
        assert response["data"]["source"] == issue_data["source"]
        assert response["data"]["type"] == issue_data["type"]
        assert response["data"]["id"]


def test_get_user_info(mock_app, mocker):
    with mock_app.app_context(), mock_app.test_request_context():
        fake_user_data = {
            "data": {
                "id": 1,
                "name": fake.name(),
                "company_id": 1,
            },
        }
        mocker.patch("src.common.utils.get_auth_header_from_request", return_value={"Authorization": "Bearer token"})
        mocker.patch("src.services.send_request", return_value=fake_user_data)
        user_info = get_user_info()
        assert user_info == fake_user_data["data"]
