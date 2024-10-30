from random import choice
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from faker import Faker
from src.common.enums import IssueType
from src.daemon import EmailDaemon  # Adjust the import based on your project structure
from src.models.entities import AuthUser
from src.models.entities import User

fake = Faker()


class TestEmailDaemon:
    @pytest.fixture
    def setup_email_daemon(self):
        # Create an instance of EmailDaemon with mocked services
        daemon = EmailDaemon()
        daemon.mail_service = MagicMock()
        daemon.pubsub_service = MagicMock()
        return daemon

    @pytest.fixture
    def auth_user(self):
        user_data = {"id": 1, "email": fake.email(), "status": choice(["ACTIVE", "INACTIVE"]), "role": choice(["user", "admin"])}
        return AuthUser(**user_data)

    @pytest.fixture
    def user(self):
        user_data = {"id": 1, "company_id": 1, "auth_id": 1, "name": fake.name(), "phone": fake.phone_number()}
        return User(**user_data)

    def test_is_user_authorized(self, setup_email_daemon, auth_user):
        # Mock get_auth_user_data to return auth_user when called
        with patch("src.daemon.get_auth_user_data", return_value=auth_user):
            user_data = setup_email_daemon.is_user_authorized(auth_user.email)
            assert user_data == auth_user

    def test_clean_email_body(self, setup_email_daemon):
        body = f"""
            <html>
                <head>
                    <title>Test Email</title>
                </head>
                <body>
                    <h1>Test Email</h1>
                    <p>This is a test email.</p>
                </body>
            </html>
        """
        expected_body = "Test Email Test Email This is a test email."
        cleaned_body = setup_email_daemon.clean_email_body(body)
        assert cleaned_body == expected_body

    def test_get_issue_type(self, setup_email_daemon):
        request_description = "Necesito asistencia para completar la solicitud de acceso al sistema, agradecería su ayuda."
        complaint_description = "Estoy muy decepcionado con el servicio, hubo varias fallas y el problema persiste."
        claim_description = "Solicito una indemnización por los daños ocasionados y una compensación por el mal servicio recibido."
        suggestion_description = "Quisiera proponer una mejora en la interfaz de usuario para facilitar el acceso a las funciones."
        praise_description = "Quiero felicitarlos, el servicio es excelente y he quedado muy satisfecho con la atención."

        assert setup_email_daemon.get_issue_type(request_description) == IssueType.REQUEST.value
        assert setup_email_daemon.get_issue_type(complaint_description) == IssueType.COMPLAINT.value
        assert setup_email_daemon.get_issue_type(claim_description) == IssueType.CLAIM.value
        assert setup_email_daemon.get_issue_type(suggestion_description) == IssueType.SUGGESTION.value
        assert setup_email_daemon.get_issue_type(praise_description) == IssueType.PRAISE.value

    def test_format_issue(self, setup_email_daemon, auth_user, user):
        # Mock get_user_data to return user when called
        with patch("src.daemon.get_user_data", return_value=user):
            email_data = {"subject": fake.sentence(), "body": fake.paragraph()}
            issue = setup_email_daemon.format_issue(auth_user, email_data)
            assert issue["type"] == IssueType.REQUEST.value
            assert issue["description"] == f"{email_data['subject']} - {email_data['body']}"
            assert issue["source"] == "EMAIL"
            assert issue["user_id"] == user.id
            assert issue["company_id"] == user.company_id
            assert issue["email"] == auth_user.email

    def test_is_valid_email(self, setup_email_daemon, auth_user):
        with patch("src.daemon.get_auth_user_data", return_value=auth_user):
            email_data = {"from": auth_user.email, "subject": fake.sentence(), "body": fake.paragraph()}
            auth_user.role = "user"
            is_valid, output_user = setup_email_daemon.is_valid_email(email_data)
            assert is_valid
            assert output_user == auth_user
