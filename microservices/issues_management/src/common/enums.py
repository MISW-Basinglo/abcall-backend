from enum import Enum


class BaseEnum(Enum):
    def __str__(self) -> str:
        return self.value


class ExceptionsMessages(BaseEnum):
    # User-related errors
    USER_NOT_REGISTERED = "User not registered."
    USER_NOT_AUTHORIZED = "User not authorized."
    USER_NOT_FOUND = "User not found."
    USER_NOT_AUTHENTICATED = "User not authenticated."
    INVALID_PASSWORD = "Invalid password."

    # Token-related errors
    TOKEN_NOT_FOUND = "Token not found."
    ERROR_DECODING_TOKEN = "Error decoding token."

    # Resource-related errors
    RESOURCE_NOT_FOUND = "Resource not found."
    RESOURCE_EXISTS = "Resource already exists."

    # Parameter-related errors
    INVALID_PARAMETER = "Invalid parameter."

    # General errors
    ERROR = "Something went wrong. Please try again later."


class MarshmallowCustomValidationMessages(BaseEnum):
    MISSING_DATA = "Missing {field}."
    INVALID_DATA = "Not a valid {field}."
    GENERIC_ERROR = "Error in {field}."


class IssueSource(BaseEnum):
    CALL = "CALL"
    EMAIL = "EMAIL"
    WEB = "WEB"
    CHATBOT = "CHATBOT"
    APP_MOBILE = "APP_MOBILE"
    OTHER = "OTHER"


class IssueType(BaseEnum):
    REQUEST = "REQUEST"
    COMPLAINT = "COMPLAINT"
    CLAIM = "CLAIM"
    SUGGESTION = "SUGGESTION"
    PRAISE = "PRAISE"


class IssueStatus(BaseEnum):
    OPEN = "OPEN"
    SCALED = "SCALED"
    CLOSED = "CLOSED"


class Permissions(BaseEnum):
    CREATE_ISSUE = "create_issue"
    VIEW_ISSUE = "view_issue"
    EDIT_ISSUE = "edit_issue"
    DELETE_ISSUE = "delete_issue"


class BasicRoles(BaseEnum):
    ADMIN = "admin"
    USER = "user"
    AGENT = "agent"
    CLIENT = "client"
