import time
from email.utils import parseaddr

from src.common.logger import logger
from src.common.utils import get_user_data
from src.services.gmail_service import GmailService as MailService


class EmailDaemon:
    def __init__(self, poll_interval=5):
        self.mail_service = MailService()
        self.poll_interval = poll_interval

    def is_valid_email(self, email_data):
        basic_validation = self.mail_service.is_valid_email(email_data)
        user_validation = self.is_user_authorized(email_data.get("from"))
        return basic_validation and user_validation

    def run(self):
        logger.info("Email daemon started.")
        while True:
            try:
                logger.info("Pulling unread emails...")
                emails = self.mail_service.fetch_unread_emails()

                if emails:
                    logger.info(f"Fetched {len(emails)} unread emails.")
                    for email in emails:
                        if self.is_valid_email(email):
                            # Publish each valid email to Pub/Sub
                            # self.pubsub_service.publish_message(str(email))
                            logger.info("Correo publicado en Pub/Sub.", email)
                        else:
                            logger.info(f"Correo descartado: {email.get('subject')}")
                            self.mail_service.mark_as_read(email.get("id"))
                else:
                    logger.info("No new emails found.")

                time.sleep(self.poll_interval)  # Wait for the next polling cycle
            except Exception as e:
                logger.error(f"Error in email daemon: {e}")

    @staticmethod
    def is_user_authorized(email) -> bool:
        extracted_email = parseaddr(email)[1]
        user_data = get_user_data(extracted_email)
        return user_data.is_valid()
