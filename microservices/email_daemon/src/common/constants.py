import os

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC")
GMAIL_CREDENTIALS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH", "src/credentials/mail_client.json")
GMAIL_TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", "src/credentials/mail_client_credentials.json")
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
GMAIL_CREDENTIALS = os.getenv("GMAIL_CREDENTIALS")
POLL_TIMEOUT = os.getenv("POLL_TIMEOUT", 5)
DAEMON_REQUEST_HEADER_VALUE = os.getenv("DAEMON_REQUEST_HEADER_VALUE", "email-daemon")
BACKEND_HOST = os.getenv("BACKEND_HOST", "http://localhost")
