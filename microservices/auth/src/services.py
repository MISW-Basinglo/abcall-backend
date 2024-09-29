from datetime import timedelta
from typing import Dict

from flask_jwt_extended import create_refresh_token
from src.common.constants import ExceptionsMessages
from src.common.constants import JWT_REFRESH_DELTA
from src.common.decorators import db_session
from src.common.exceptions import ResourceNotFoundException
from src.common.exceptions import UserNotAuthorizedException
from src.common.utils import generate_token
from src.models.entities import TokenResponseEntity
from src.models.user import User
from src.serializers import TokenSerializer
from src.serializers import UserLoginSerializer


def authenticate(data: Dict):
    login_data = UserLoginSerializer().load_with_exception(data)
    user = get_user_by_email(login_data["email"])

    if not user:
        raise ResourceNotFoundException(ExceptionsMessages.USER_NOT_REGISTERED.value)

    if not user.check_password(login_data["password"]):
        raise UserNotAuthorizedException(ExceptionsMessages.INVALID_PASSWORD.value)

    access_token = generate_token(user)
    refresh_token = create_refresh_token(user.id, expires_delta=timedelta(days=JWT_REFRESH_DELTA))

    tokens = TokenResponseEntity(access_token=access_token, refresh_token=refresh_token)
    token_serializer = TokenSerializer()

    return token_serializer.dump(tokens)


def refresh_access_token(user_identity):
    user = get_user_by_id(user_identity)
    if not user:
        raise UserNotAuthorizedException(ExceptionsMessages.USER_NOT_REGISTERED.value)
    new_access_token = generate_token(user)
    return {"access_token": new_access_token}


@db_session
def get_user_by_email(session, email):
    user = session.query(User).filter(User.email == email).first()
    return user


@db_session
def get_user_by_id(session, user_id):
    user = session.query(User).filter(User.id == user_id).first()
    return user
