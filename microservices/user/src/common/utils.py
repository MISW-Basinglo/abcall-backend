# app/utils.py
import random

from flask import request as flask_request
from flask_jwt_extended import get_jwt
from src.common.enums import ExceptionsMessages
from src.common.exceptions import CustomException
from src.common.logger import logger


def format_exception_message(exception: Exception) -> str:
    cause = str(exception.__cause__) if exception.__cause__ else str(exception)

    if "DETAIL:" in cause:
        detail_message = cause.split("DETAIL:")[-1].strip()
        return detail_message.replace("\n", " ").capitalize()

    return cause
