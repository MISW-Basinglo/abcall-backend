# app/utils.py
from datetime import timedelta
from typing import Dict
from typing import List

from flask_jwt_extended import create_access_token
from src.common.constants import JWT_ACCESS_DELTA
from src.models.user import User


def generate_token(user: User) -> str:
    permissions: List[str] = user.get_permissions()
    role: str = user.get_roles()[0]

    additional_claims: Dict = {"role": role, "permissions": permissions}

    access_token: str = create_access_token(identity=user.id, additional_claims=additional_claims, expires_delta=timedelta(hours=JWT_ACCESS_DELTA))

    return access_token
