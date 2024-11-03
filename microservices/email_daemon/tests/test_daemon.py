from random import choice
from unittest.mock import patch

import pytest
from faker import Faker
from src.common.enums import IssueType
from src.daemon import EmailDaemon
from src.models.entities import AuthUser
from src.models.entities import User

fake = Faker()


class TestEmailDaemon:
    @pytest.fixture
    def setup_email_daemon(self):
        with patch("src.daemon.MailService", autospec=True) as MockMailService, patch("src.daemon.PubSubService", autospec=True) as MockPubSubService:
            daemon = EmailDaemon()
            daemon.mail_service = MockMailService()
            daemon.pubsub_service = MockPubSubService()
            yield daemon

    @pytest.fixture
    def auth_user(self):
        user_data = {"id": 1, "email": fake.email(), "status": choice(["ACTIVE", "INACTIVE"]), "role": "user"}
        return AuthUser(**user_data)

    @pytest.fixture
    def user(self):
        user_data = {"id": 1, "company_id": 1, "auth_id": 1, "name": fake.name(), "phone": fake.phone_number()}
        return User(**user_data)

    def test_is_user_authorized(self, setup_email_daemon, auth_user):
        with patch("src.daemon.get_auth_user_data", return_value=auth_user):
            user_data = setup_email_daemon.is_user_authorized(auth_user.email)
            assert user_data == auth_user

    def test_clean_email_body(self, setup_email_daemon):
        body = """
            <html>
                <head><title>Test Email</title></head>
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
        descriptions = {
            "Necesito asistencia para completar la solicitud de acceso al sistema, agradecería su ayuda.": IssueType.REQUEST.value,
            "Estoy muy decepcionado con el servicio, hubo varias fallas y el problema persiste.": IssueType.COMPLAINT.value,
            "Solicito una indemnización por los daños ocasionados y una compensación por el mal servicio recibido.": IssueType.CLAIM.value,
            "Quisiera proponer una mejora en la interfaz de usuario para facilitar el acceso a las funciones.": IssueType.SUGGESTION.value,
            "Quiero felicitarlos, el servicio es excelente y he quedado muy satisfecho con la atención.": IssueType.PRAISE.value,
        }

        for description, expected_type in descriptions.items():
            assert setup_email_daemon.get_issue_type(description) == expected_type

    def test_format_issue(self, setup_email_daemon, auth_user, user):
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
            email_data = {"from": auth_user.email, "subject": "Fake test subject", "body": "Fake body text"}
            is_valid, output_user = setup_email_daemon.is_valid_email(email_data)
            assert is_valid
            assert output_user == auth_user
