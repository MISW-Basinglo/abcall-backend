import json
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from src.common.constants import GMAIL_CREDENTIALS
from src.common.constants import GMAIL_SCOPES
from src.common.logger import logger
from src.services.base import BaseMailService


class GmailService(BaseMailService):
    credentials = None

    def __init__(self):
        self.credentials = self.authenticate()
        self.service = build("gmail", "v1", credentials=self.credentials)

    def authenticate(self):
        return self.get_gmail_credentials()

    @staticmethod
    def get_gmail_credentials():
        creds = None
        google_credentials = GMAIL_CREDENTIALS
        if google_credentials:
            creds = Credentials.from_authorized_user_info(eval(google_credentials), GMAIL_SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                os.environ[GMAIL_CREDENTIALS] = json.dumps(creds.to_json())  # Storing the new token in env variable
            else:
                raise ValueError("Invalid credentials. Please, authenticate again.")
        return creds

    def fetch_unread_emails(self):
        try:
            result = self.service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
            messages = result.get("messages", [])

            email_data = []
            for message in messages:
                msg = self.service.users().messages().get(userId="me", id=message["id"]).execute()
                email_data.append(
                    {
                        "id": msg["id"],
                        "subject": self.get_header(msg["payload"]["headers"], "Subject"),
                        "from": self.get_header(msg["payload"]["headers"], "From"),
                        "body": msg["snippet"],
                    },
                )
            return email_data
        except Exception as e:
            logger.info(f"Error fetching unread emails: {e}")
            return []

    def fetch_emails(self, query):
        pass

    def mark_as_read(self, message_id):
        try:
            self.service.users().messages().modify(userId="me", id=message_id, body={"removeLabelIds": ["UNREAD"]}).execute()
        except Exception as e:
            logger.error(f"Error marking email as read: {e}")

    @staticmethod
    def get_header(headers, name):
        for header in headers:
            if header["name"] == name:
                return header["value"]
        return None
