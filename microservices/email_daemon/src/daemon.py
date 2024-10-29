import re
import time
from email.utils import parseaddr
from typing import Dict

from bs4 import BeautifulSoup
from src.common.enums import IssueType
from src.common.logger import logger
from src.common.utils import get_auth_user_data
from src.common.utils import get_user_data
from src.models.entities import AuthUser
from src.models.entities import IssueEntity
from src.serializers import IssueCreateSerializer
from src.services.gmail_service import GmailService as MailService


class EmailDaemon:
    def __init__(self, poll_interval=5):
        self.mail_service = MailService()
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
            raise ValueError("El contenido del correo debe ser una cadena de texto.")

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

        # Remove URLs, email addresses, and clean up multiple spaces or newlines
        body = re.sub(r"https?://\S+|www\.\S+", "", body)
        body = re.sub(r"\S+@\S+", "", body)
        body = re.sub(r"\n\s*\n", "\n", body)
        body = re.sub(r"[ \t]+", " ", body)

        return body.strip()

    @staticmethod
    def get_issue_type(description):
        description = description.lower()
        keywords = IssueType.get_keywords()
        issue_type = IssueType.REQUEST

        for t, words in keywords.items():
            for word in words:
                if re.search(word, description):
                    issue_type = t
                    break
        return issue_type

    def format_issue(self, user, email_data) -> Dict:
        user_data = get_user_data(user.id)
        description = email_data["body"]
        issue_type = self.get_issue_type(description)
        source = "EMAIL"
        issue_entity = IssueEntity(
            type=issue_type,
            description=description,
            source=source,
            user_id=user_data.id,
            company_id=user_data.company_id,
        )
        return IssueCreateSerializer().dump(issue_entity)

    def run(self):
        logger.info("Email daemon started.")
        while True:
            logger.info("Pulling unread emails...")
            emails = self.mail_service.fetch_unread_emails()
            for email in emails:
                try:
                    email["body"] = self.clean_email_body(email.get("body"))
                    is_valid, user = self.is_valid_email(email)
                    if is_valid:
                        issue_body = self.format_issue(user, email)
                        # TODO: Publish the issue_body to a Pub/Sub topic
                        logger.info("Correo publicado en Pub/Sub.", issue_body)
                    else:
                        logger.info(f"Correo descartado: {email.get('subject')}")
                        self.mail_service.mark_as_read(email.get("id"))
                except Exception as e:
                    logger.error(f"Error processing emails: {e}")
                    pass
            else:
                logger.info("No new emails found.")
            time.sleep(self.poll_interval)  # Wait for the next polling cycle
