from datetime import datetime
from datetime import timedelta
from typing import Dict

from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from src.common.constants import JWT_REFRESH_DELTA
from src.common.enums import ExceptionsMessages
from src.common.enums import UserAuthStatus
from src.common.exceptions import CustomException
from src.common.exceptions import ResourceNotFoundException
from src.common.exceptions import UserNotAuthorizedException
from src.common.logger import logger
from src.common.utils import generate_token
from src.models.entities import AuditAuthUser
from src.models.entities import GenericResponseEntity
from src.models.entities import TokenResponseEntity
from src.repositories.auth_repository import UserAuthRepository
from src.serializers.serializers import AuditAuthUserSerializer
from src.serializers.serializers import GenericResponseSerializer
from src.serializers.serializers import TokenSerializer
from src.serializers.serializers import UserAuthUpdateSerializer
from src.serializers.serializers import UserCreateSerializer
from src.serializers.serializers import UserLoginSerializer
from src.serializers.serializers import UserRetrieveSerializer


def authenticate(data: Dict):
    auth_repository = UserAuthRepository()
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
    auth_repository = UserAuthRepository()
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
    email = claims.get("email")
    if not any([role, permissions, email]):
        logger.error(ExceptionsMessages.ERROR_DECODING_TOKEN.value)
        raise CustomException(ExceptionsMessages.ERROR_DECODING_TOKEN.value)
    audit_auth = AuditAuthUser(user_id=user_id, role=role, permissions=permissions, email=email)
    audit_serializer = AuditAuthUserSerializer()
    return audit_serializer.dump(audit_auth)


def create_user_auth(data):
    auth_repository = UserAuthRepository()
    data["status"] = data.get("status", UserAuthStatus.PENDING.value)
    data = UserCreateSerializer().load(data)
    auth_repository.set_serializer(UserRetrieveSerializer)
    user_auth = auth_repository.create(data)
    response_entity = GenericResponseEntity(data=user_auth)
    response = GenericResponseSerializer().dump(response_entity)
    return response


def update_user_auth(auth_id, data):
    data = UserAuthUpdateSerializer().load(data)
    auth_repository = UserAuthRepository()
    auth_repository.set_serializer(UserRetrieveSerializer)
    user_auth = auth_repository.update(auth_id, data)
    response_entity = GenericResponseEntity(data=user_auth)
    return GenericResponseSerializer().dump(response_entity)


def delete_auth_user_service(auth_id: int):
    auth_repository = UserAuthRepository()
    auth_repository.delete(auth_id)


def get_auth_user_by_field_service(params: list):
    auth_repository = UserAuthRepository()
    auth_repository.set_serializer(UserRetrieveSerializer)
    user = auth_repository.get_by_field(*params)
    response_entity = GenericResponseEntity(data=user)
    response = GenericResponseSerializer().dump(response_entity)
    return response
