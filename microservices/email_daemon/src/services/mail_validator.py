import re
from email.utils import parseaddr
from typing import Any
from typing import Dict


class MailValidator:
    DEFAULT_SPAM_WORDS = ["gana", "gratis", "dinero", "premio", "oferta", "imperdible", "bono"]
    DEFAULT_BODY_SPAM_THRESHOLD = 2

    def validate_email(self, email_data: Dict[str, Any]) -> bool:
        """Validates the structure of the email to decide whether it should be processed or rejected."""

        # Check if required fields are present
        required_fields = {"from", "subject", "body"}
        data_keys = set(email_data.keys())
        if required_fields - data_keys:
            return False

        validations = [self.is_valid_email_address(email_data["from"]), self.is_valid_subject(email_data["subject"]), self.is_valid_body(email_data["body"])]

        return all(validations)

    def is_valid_email_address(self, email: str) -> bool:
        """Validates the email address format using a regular expression."""
        extracted_email = parseaddr(email)[1]
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, extracted_email) is not None

    def is_valid_subject(self, subject: str) -> bool:
        """Checks the subject for common spam indicators."""
        subject = subject.lower()
        return not any(indicator in subject for indicator in self.DEFAULT_SPAM_WORDS)

    def is_valid_body(self, body: str) -> bool:
        """Checks the email body for common spam content."""
        body = body.lower()
        spam_count = sum(body.count(word) for word in self.DEFAULT_SPAM_WORDS)
        return spam_count < self.DEFAULT_BODY_SPAM_THRESHOLD
