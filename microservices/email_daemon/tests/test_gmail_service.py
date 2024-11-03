from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from src.services.gmail_service import GmailService


class TestGmailService:
    @pytest.fixture
    def gmail_service(self):
        """Fixture to create an instance of GmailService with mocked dependencies."""
        with patch("src.services.gmail_service.build") as mock_build, patch("src.services.gmail_service.GmailService.get_gmail_credentials") as mock_get_gmail_credentials:
            # Mock the credentials and service
            mock_creds = MagicMock()
            mock_get_gmail_credentials.return_value = mock_creds

            # Mock the Gmail API service
            mock_service = MagicMock()
            mock_build.return_value = mock_service

            # Instantiate the GmailService
            gmail_service_instance = GmailService()

            # Replace the service attribute with our mock
            gmail_service_instance.service = mock_service

            yield gmail_service_instance

    def test_get_gmail_credentials_valid(self):
        """Test getting valid Gmail credentials."""
        with patch("src.services.gmail_service.GmailService.get_gmail_credentials") as mock_get_gmail_credentials:
            mock_creds = MagicMock()
            mock_creds.valid = True
            mock_get_gmail_credentials.return_value = mock_creds

            service = GmailService()
            assert service.credentials == mock_creds

    def test_fetch_unread_emails(self, gmail_service):
        """Test fetching unread emails."""
        gmail_service.service.users().messages().list.return_value.execute.return_value = {"messages": [{"id": "1"}]}
        gmail_service.service.users().messages().get.return_value.execute.return_value = {
            "id": "1",
            "payload": {"headers": [{"name": "Subject", "value": "Test Subject"}, {"name": "From", "value": "test@example.com"}]},
            "snippet": "This is a test.",
        }

        emails = gmail_service.fetch_unread_emails()
        assert len(emails) == 1
        assert emails[0]["subject"] == "Test Subject"
        assert emails[0]["from"] == "test@example.com"

    def test_fetch_unread_emails_empty(self, gmail_service):
        """Test fetching unread emails when there are none."""
        # Mock the response to return no messages
        gmail_service.service.users().messages().list.return_value.execute.return_value = {"messages": []}

        emails = gmail_service.fetch_unread_emails()
        assert emails == []

    def test_mark_as_read(self, gmail_service):
        """Test marking an email as read."""
        with patch("src.services.gmail_service.logger") as mock_logger:
            message_id = "test_id"
            gmail_service.mark_as_read(message_id)

            gmail_service.service.users().messages().modify.assert_called_once_with(userId="me", id=message_id, body={"removeLabelIds": ["UNREAD"]})
            mock_logger.error.assert_not_called()
