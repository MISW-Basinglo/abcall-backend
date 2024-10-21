from src.common.utils import format_exception_message
from src.models.entities import AuthUser

auth_user = AuthUser


def test_format_exception_message_no_detail():
    exception = Exception("Some error occurred")
    result = format_exception_message(exception)
    assert result == "Some error occurred"


def test_format_exception_message_with_detail():
    exception = Exception("ERROR: Something went wrong. DETAIL: Invalid input detected")
    result = format_exception_message(exception)
    assert result == "Invalid input detected"


def test_format_exception_message_with_cause():
    cause_exception = Exception("Root cause")
    exception = Exception("Some error")
    exception.__cause__ = cause_exception
    result = format_exception_message(exception)
    assert result == "Root cause"
