from functools import wraps
from http import HTTPStatus

from src.common.enums import ExceptionsMessages
from src.common.exceptions import CustomException
from src.common.exceptions import InvalidParameterException
from src.common.exceptions import ResourceExistsException
from src.common.exceptions import ResourceNotFoundException
from src.common.exceptions import TokenNotFoundException
from src.common.exceptions import UserNotAuthorizedException
from src.common.logger import logger


def handle_exceptions(func):
    """
    Decorator to handle exceptions
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        status_code = HTTPStatus.OK
        error = ""
        exception_cause = ""
        try:
            return func(*args, **kwargs)
        except ResourceNotFoundException as e:
            status_code = HTTPStatus.NOT_FOUND
            error = str(e)
        except InvalidParameterException as e:
            status_code = HTTPStatus.BAD_REQUEST
            error = str(e)
        except UserNotAuthorizedException as e:
            status_code = HTTPStatus.UNAUTHORIZED
            error = str(e)
        except ResourceExistsException as e:
            status_code = HTTPStatus.CONFLICT
            error = str(e)
        except TokenNotFoundException as e:
            status_code = HTTPStatus.FORBIDDEN
            error = str(e)
        except CustomException as e:
            status_code = e.status_code
            error = str(e)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            error = str(e)
        finally:
            if status_code >= HTTPStatus.BAD_REQUEST:
                logger.error(f"Error in {func.__name__}: {error}")
                if status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
                    error = ExceptionsMessages.ERROR.value
                response_object = {
                    "status": "error",
                    "msg": error,
                }
                return response_object, status_code

    return wrapper
