from datetime import datetime
from datetime import timedelta
from typing import Dict

from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from src.common.constants import ExceptionsMessages
from src.common.constants import JWT_REFRESH_DELTA
from src.common.decorators import db_session
from src.common.exceptions import CustomException
from src.common.exceptions import ResourceNotFoundException
from src.common.exceptions import UserNotAuthorizedException
from src.common.logger import logger
from src.common.utils import generate_token
from src.models.auth import UserAuth
from src.models.entities import AuditAuthUser
from src.models.entities import TokenResponseEntity
from src.serializers import AuditAuthUserSerializer
from src.serializers import TokenSerializer
from src.serializers import UserLoginSerializer


def authenticate(data: Dict):
    login_data = UserLoginSerializer().load_with_exception(data)
    user_auth = get_user_by_email(login_data["email"])

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
    update_auth(user_auth.id, {"last_login": datetime.now()})
    return token_serializer.dump(tokens)


def refresh_access_token(user_identity):
    user_auth = get_user_by_id(user_identity)
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


@db_session
def get_user_by_email(session, email):
    user_auth = session.query(UserAuth).filter(UserAuth.email == email).first()
    return user_auth


@db_session
def get_user_by_id(session, user_id):
    user_auth = session.query(UserAuth).filter(UserAuth.id == user_id).first()
    return user_auth


@db_session
def update_auth(session, user_id, data):
    user_auth = session.query(UserAuth).filter(UserAuth.id == user_id).first()
    if not user_auth:
        logger.error(ExceptionsMessages.USER_NOT_REGISTERED.value)
        raise ResourceNotFoundException(ExceptionsMessages.USER_NOT_REGISTERED.value)
    for key, value in data.items():
        setattr(user_auth, key, value)
    session.commit()
    return user_auth
