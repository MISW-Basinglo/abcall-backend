from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from src.services.gmail_service import GmailService


class TestGmailService:
    @pytest.fixture
    def gmail_service(self):
        """Fixture to create an instance of GmailService."""
        with patch("src.services.gmail_service.build") as mock_build:
            # Mock the service returned by the build function
            mock_service = MagicMock()
            mock_build.return_value = mock_service
            yield GmailService()

    @patch("src.services.gmail_service.GmailService.get_gmail_credentials")
    def test_get_gmail_credentials_valid(self, mock_get_gmail_credentials):
        """Test getting valid Gmail credentials."""
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_get_gmail_credentials.return_value = mock_creds

        service = GmailService()
        assert service.credentials == mock_creds

    @patch("src.services.gmail_service.GmailService.fetch_unread_emails")
    def test_fetch_unread_emails(self, mock_fetch_unread_emails, gmail_service):
        """Test fetching unread emails."""
        mock_fetch_unread_emails.return_value = [{"id": "1", "subject": "Test Subject", "from": "test@example.com", "body": "This is a test."}]

        emails = gmail_service.fetch_unread_emails()
        assert len(emails) == 1
        assert emails[0]["subject"] == "Test Subject"
        assert emails[0]["from"] == "test@example.com"

    @patch("src.services.gmail_service.GmailService.fetch_unread_emails", return_value=[])
    def test_fetch_unread_emails_empty(self, mock_fetch_unread_emails, gmail_service):
        """Test fetching unread emails when there are none."""
        emails = gmail_service.fetch_unread_emails()
        assert emails == []

    @patch("src.services.gmail_service.logger")
    @patch("src.services.gmail_service.GmailService.mark_as_read")
    def test_mark_as_read(self, mock_mark_as_read, mock_logger, gmail_service):
        """Test marking an email as read."""
        message_id = "test_id"
        gmail_service.mark_as_read(message_id)
        mock_mark_as_read.assert_called_once_with(message_id)
