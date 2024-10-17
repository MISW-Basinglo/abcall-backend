from datetime import datetime
from datetime import timedelta
from typing import Dict

from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from src.common.constants import JWT_REFRESH_DELTA
from src.common.enums import ExceptionsMessages
from src.common.exceptions import CustomException
from src.common.exceptions import ResourceNotFoundException
from src.common.exceptions import UserNotAuthorizedException
from src.common.logger import logger
from src.common.utils import generate_token
from src.models.entities import AuditAuthUser
from src.models.entities import TokenResponseEntity
from src.repositories.auth_repository import UserAuthRepository
from src.serializers.auth_serializers import AuditAuthUserSerializer
from src.serializers.auth_serializers import TokenSerializer
from src.serializers.auth_serializers import UserLoginSerializer

auth_repository = UserAuthRepository()


def authenticate(data: Dict):
    login_data = UserLoginSerializer().load(data)
    user_auth = auth_repository.get_by_field("email", login_data["email"])

    if not user_auth:
        logger.error(ExceptionsMessages.USER_NOT_REGISTERED.value)
        raise ResourceNotFoundException(ExceptionsMessages.USER_NOT_REGISTERED.value)

    if not user_auth.check_password(login_data["password"]):
        logger.error(ExceptionsMessages.INVALID_PASSWORD.value)
        raise UserNotAuthorizedException(ExceptionsMessages.INVALID_PASSWORD.value)

    access_token = generate_token(user_auth)
    refresh_token = create_refresh_token(user_auth.id, expires_delta=timedelta(days=JWT_REFRESH_DELTA))

    tokens = TokenResponseEntity(access_token=access_token, refresh_token=refresh_token)
    token_serializer = TokenSerializer()
    auth_repository.update(user_auth.id, {"last_login": datetime.now()})
    return token_serializer.dump(tokens)


def refresh_access_token(user_identity):
    user_auth = auth_repository.get_by_field("id", user_identity)
    if not user_auth:
        logger.error(ExceptionsMessages.USER_NOT_REGISTERED.value)
        raise UserNotAuthorizedException(ExceptionsMessages.USER_NOT_REGISTERED.value)
    new_access_token = generate_token(user_auth)
    return {"access_token": new_access_token}


def audit_decode_token(user_id):
    claims = get_jwt()
    role = claims.get("role")
    permissions = claims.get("permissions")
    if not role or not permissions:
        logger.error(ExceptionsMessages.ERROR_DECODING_TOKEN.value)
        raise CustomException(ExceptionsMessages.ERROR_DECODING_TOKEN.value)
    audit_auth = AuditAuthUser(user_id=user_id, role=role, permissions=permissions)
    audit_serializer = AuditAuthUserSerializer()
    return audit_serializer.dump(audit_auth)
