from functools import wraps
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError
from src.common.constants import DISABLE_PERMISSIONS_VALIDATIONS
from src.common.enums import ExceptionsMessages
from src.common.exceptions import CustomException
from src.common.exceptions import InvalidParameterException
from src.common.exceptions import ResourceExistsException
from src.common.exceptions import ResourceNotFoundException
from src.common.exceptions import TokenNotFoundException
from src.common.exceptions import UserNotAuthorizedException
from src.common.logger import logger
from src.common.utils import decode_token


def handle_exceptions(func):
    """
    Decorator to handle exceptions
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        status_code = HTTPStatus.OK
        error = ""
        try:
            return func(*args, **kwargs)
        except ResourceNotFoundException as e:
            status_code = HTTPStatus.NOT_FOUND
            error = str(e)
        except InvalidParameterException as e:
            status_code = HTTPStatus.BAD_REQUEST
            error = str(e)
        except (UserNotAuthorizedException, NoAuthorizationError) as e:
            status_code = HTTPStatus.UNAUTHORIZED
            error = str(e)
        except ResourceExistsException as e:
            status_code = HTTPStatus.CONFLICT
            error = str(e)
        except TokenNotFoundException as e:
            status_code = HTTPStatus.FORBIDDEN
            error = str(e)
        except ExpiredSignatureError as e:
            status_code = HTTPStatus.UNAUTHORIZED
            error = ExceptionsMessages.USER_NOT_AUTHENTICATED.value
        except CustomException as e:
            status_code = e.status_code
            error = str(e)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            error = ExceptionsMessages.ERROR.value
        finally:
            if status_code >= HTTPStatus.BAD_REQUEST:
                response_object = {
                    "status": "error",
                    "msg": error,
                }
                logger.error(f"Error in {func.__name__}: {error}")
                return response_object, status_code

    return wrapper


def validate_permissions(permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # user_id = get_jwt_identity()
            # user = decode_token(user_id)
            # validations = [
            #     bool(user),
            #     user.has_permissions(permissions),
            # ]
            # if not all(validations) and not DISABLE_PERMISSIONS_VALIDATIONS:
            #     raise UserNotAuthorizedException(ExceptionsMessages.USER_NOT_AUTHORIZED.value)
            return func(*args, **kwargs)

        return wrapper

    return decorator
