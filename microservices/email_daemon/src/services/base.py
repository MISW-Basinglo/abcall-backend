from abc import ABC
from abc import abstractmethod

from src.services.mail_validator import MailValidator


class BaseMailService(ABC):
    mail_validator = MailValidator()

    @abstractmethod
    def authenticate(self):
        """Autentica el servicio de email."""
        pass

    @abstractmethod
    def mark_as_read(self, email_id):
        """Marca un correo como leído."""
        pass

    @abstractmethod
    def fetch_emails(self, query):
        """Obtiene los correos del servicio de email."""
        pass

    @abstractmethod
    def fetch_unread_emails(self):
        """Obtiene los correos no leídos del servicio de email."""
        pass

    def is_valid_email(self, email_data):
        """Valida la estructura del correo para decidir si debe ser procesado o rechazado."""
        return self.mail_validator.validate_email(email_data)
