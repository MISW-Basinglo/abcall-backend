import re
import time
from email.utils import parseaddr

from bs4 import BeautifulSoup
from src.common.enums import IssueType
from src.common.logger import logger
from src.common.utils import get_auth_user_data
from src.common.utils import get_user_data
from src.models.entities import AuthUser
from src.models.entities import IssueEntity
from src.serializers import IssueCreateSerializer
from src.services.gmail_service import GmailService as MailService
from src.services.pubsub_service import PubSubService


class EmailDaemon:
    def __init__(self, poll_interval=5):
        self.mail_service = MailService()
        self.pubsub_service = PubSubService()
        self.poll_interval = poll_interval

    def is_valid_email(self, email_data):
        basic_validation = self.mail_service.is_valid_email(email_data)
        user = self.is_user_authorized(email_data.get("from"))
        return basic_validation and user.is_valid(), user

    @staticmethod
    def is_user_authorized(email) -> AuthUser:
        extracted_email = parseaddr(email)[1]
        user_data = get_auth_user_data(extracted_email)
        return user_data

    @staticmethod
    def clean_email_body(body: str) -> str:
        """
        Cleans the email body by removing unnecessary information, headers, and formatting.
        :param body: The raw email body as a string.
        :return: The cleaned email body as a string.
        """
        if not isinstance(body, str):
            raise ValueError("Mail body must be a string.")

        # Parse HTML if present and extract text
        body = BeautifulSoup(body, "html.parser").get_text(separator=" ")

        # Remove zero-width characters and extra whitespace
        body = re.sub(r"[\u200b\u200c\u200d\u2060]+", "", body)
        body = re.sub(r"\s+", " ", body).strip()

        # Remove headers commonly found in forwarded or replied email bodies
        body = re.split(r"\b(?:From|Sent|To|Subject|De|Para|Enviado):\b", body, flags=re.IGNORECASE)[0]

        # Remove common email client signatures and any residual whitespace
        body = re.sub(r"Get\s+Outlook\s+for\s+\w+|Sent\s+from\s+my\s+\w+", "", body, flags=re.IGNORECASE)
        body = re.sub(r"(Forwarded message|Mensaje reenviado):", "", body, flags=re.IGNORECASE)

        return body.strip()

    @staticmethod
    def get_issue_type(description):
        description = description.lower()
        keywords = IssueType.get_keywords()
        issue_type = IssueType.REQUEST.value

        for t, words in keywords.items():
            for word in words:
                if re.search(word, description):
                    issue_type = t.value
                    break
        return issue_type

    def format_issue(self, user, email_data) -> dict:
        user_data = get_user_data(user.id)
        description = f"{email_data.get('subject')} - {email_data.get('body')}"
        issue_type = self.get_issue_type(description)
        source = "EMAIL"
        issue_entity = IssueEntity(type=issue_type, description=description, source=source, user_id=user_data.id, company_id=user_data.company_id, email=user.email)
        return IssueCreateSerializer().dump(issue_entity)

    def run(self):
        logger.info("Email daemon started.")
        while True:
            emails = self.mail_service.fetch_unread_emails()
            for email in emails:
                try:
                    email["body"] = self.clean_email_body(email.get("body"))
                    is_valid, user = self.is_valid_email(email)
                    if is_valid:
                        issue_body = self.format_issue(user, email)
                        message_id = self.pubsub_service.publish_message(issue_body)
                        logger.info("Email published into Google Pub/Sub:" + message_id)
                    else:
                        logger.info(f"Email discarded: {email.get('subject')}")
                except Exception as e:
                    logger.error(f"Error processing email: {e}")
                finally:
                    self.mail_service.mark_as_read(email.get("id"))

            else:
                logger.info("No emails to process.")
            time.sleep(self.poll_interval)  # Wait for the next polling cycle
