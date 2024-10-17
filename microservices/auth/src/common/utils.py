# app/utils.py
from datetime import timedelta
from typing import Dict
from typing import List

from flask_jwt_extended import create_access_token
from src.common.constants import JWT_ACCESS_DELTA
from src.models.auth import UserAuth


def generate_token(user_auth: UserAuth) -> str:
    permissions: List[str] = user_auth.get_permissions()
    role: str = user_auth.get_role()

    additional_claims: Dict = {"role": role, "permissions": permissions}

    access_token: str = create_access_token(identity=user_auth.id, additional_claims=additional_claims, expires_delta=timedelta(hours=JWT_ACCESS_DELTA))

    return access_token


def format_exception_message(exception: Exception) -> str:
    cause = str(exception.__cause__) if exception.__cause__ else str(exception)

    if "DETAIL:" in cause:
        detail_message = cause.split("DETAIL:")[-1].strip()
        return detail_message.replace("\n", " ").capitalize()

    return cause
