import pytest
from src.services.mail_validator import MailValidator


class TestMailValidator:
    @pytest.fixture
    def validator(self):
        """Fixture to provide an instance of MailValidator for testing."""
        return MailValidator()

    def test_validate_email_valid(self, validator):
        """Test valid email data."""
        email_data = {"from": "test@example.com", "subject": "Hello World", "body": "This is a valid email body."}
        assert validator.validate_email(email_data) is True

    def test_validate_email_missing_fields(self, validator):
        """Test email data with missing fields."""
        email_data = {
            "from": "test@example.com",
            "subject": "Hello World",
            # 'body' is missing
        }
        assert validator.validate_email(email_data) is False

    def test_validate_email_invalid_address(self, validator):
        """Test email data with an invalid email address."""
        email_data = {"from": "invalid_email", "subject": "Hello World", "body": "This is a valid email body."}
        assert validator.validate_email(email_data) is False

    def test_validate_email_subject_spam(self, validator):
        """Test email data with spam in the subject."""
        email_data = {"from": "test@example.com", "subject": "Gana un premio", "body": "This is a valid email body."}
        assert validator.validate_email(email_data) is False

    def test_validate_email_body_spam(self, validator):
        """Test email data with spam in the body."""
        email_data = {"from": "test@example.com", "subject": "Hello World", "body": "Gana dinero ahora"}
        assert validator.validate_email(email_data) is False

    def test_validate_email_body_spam_threshold(self, validator):
        """Test email data with spam words below the threshold."""
        email_data = {"from": "test@example.com", "subject": "Hello World", "body": "This is a valid body with bono."}
        assert validator.validate_email(email_data) is True

    def test_is_valid_email_address_valid(self, validator):
        """Test valid email addresses."""
        assert validator.is_valid_email_address("test@example.com") is True
        assert validator.is_valid_email_address("user.name+tag+sorting@example.com") is True

    def test_is_valid_email_address_invalid(self, validator):
        """Test invalid email addresses."""
        assert validator.is_valid_email_address("invalid_email") is False
        assert validator.is_valid_email_address("user@.com") is False

    def test_is_valid_subject_no_spam(self, validator):
        """Test subject with no spam indicators."""
        assert validator.is_valid_subject("Regular Subject") is True

    def test_is_valid_subject_with_spam(self, validator):
        """Test subject with spam indicators."""
        assert validator.is_valid_subject("Gana dinero") is False

    def test_is_valid_body_below_threshold(self, validator):
        """Test body with spam words below threshold."""
        assert validator.is_valid_body("This is a valid body.") is True
        assert validator.is_valid_body("This is a body with bono.") is True

    def test_is_valid_body_above_threshold(self, validator):
        """Test body with spam words above threshold."""
        assert validator.is_valid_body("Gana dinero imperdible") is False  # Adjust words for testing
