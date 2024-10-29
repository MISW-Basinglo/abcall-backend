import time
from email.utils import parseaddr
from typing import Tuple

from src.common.logger import logger
from src.common.utils import get_auth_user_data
from src.common.utils import get_user_data
from src.models.entities import AuthUser
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

    def format_issue_body(self, user, email_data):
        email_address = user.email
        user = get_user_data(user.id)
        return {}

    def run(self):
        logger.info("Email daemon started.")
        while True:
            logger.info("Pulling unread emails...")
            emails = self.mail_service.fetch_unread_emails()
            for email in emails:
                try:
                    logger.info(f"Fetched {len(emails)} unread emails.")
                    is_valid, user = self.is_valid_email(email)
                    if is_valid:
                        issue_body = self.format_issue_body(user, email)
                        logger.info("Correo publicado en Pub/Sub.", email)
                        logger.info(f"Correo publicado en Pub/Sub: {email.get('subject')}")
                    else:
                        logger.info(f"Correo descartado: {email.get('subject')}")
                        self.mail_service.mark_as_read(email.get("id"))
                except Exception as e:
                    logger.error(f"Error processing emails: {e}")
                    pass
            else:
                logger.info("No new emails found.")
            time.sleep(self.poll_interval)  # Wait for the next polling cycle
