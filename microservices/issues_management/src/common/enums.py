from enum import Enum


class ExceptionsMessages(Enum):
    # User-related errors
    USER_NOT_REGISTERED = "User not registered."
    USER_NOT_AUTHORIZED = "User not authorized."
    USER_NOT_FOUND = "User not found."
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


class MarshmallowCustomValidationMessages(Enum):
    MISSING_DATA = "Missing {field}."
    INVALID_DATA = "Not a valid {field}."
    GENERIC_ERROR = "Error in {field}."


class IssueSource(Enum):
    CALL = "call"
    EMAIL = "email"
    APP_WEB = "web"
    CHATBOT = "chatbot"
    APP_MOBILE = "app_mobile"
    OTHER = "other"


class IssueType(Enum):
    REQUEST = "request"
    COMPLAINT = "complaint"
    CLAIM = "claim"
    SUGGESTION = "suggestion"
    PRAISE = "praise"


class IssueStatus(Enum):
    OPEN = "open"
    SCALED = "scaled"
    CLOSED = "closed"


class Permissions(Enum):
    CREATE_ISSUE = "create_issue"
    VIEW_ISSUE = "view_issue"
    EDIT_ISSUE = "edit_issue"
    DELETE_ISSUE = "delete_issue"
