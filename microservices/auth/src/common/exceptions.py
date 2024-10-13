from src.common.constants import ExceptionsMessages


class InvalidParameterException(Exception):
    def __init__(self, message):
        super(InvalidParameterException, self).__init__(message)


class ResourceExistsException(Exception):
    def __init__(self, message):
        super(ResourceExistsException, self).__init__(message)


class ResourceNotFoundException(Exception):
    def __init__(self, message):
        super(ResourceNotFoundException, self).__init__(message)


class UserNotAuthorizedException(Exception):
    def __init__(self, message=ExceptionsMessages.USER_NOT_AUTHORIZED.value):
        super(UserNotAuthorizedException, self).__init__(message)


class TokenNotFoundException(Exception):
    def __init__(self, message=ExceptionsMessages.TOKEN_NOT_FOUND.value):
        super(TokenNotFoundException, self).__init__(message)


class CustomException(Exception):
    def __init__(self, message=ExceptionsMessages.ERROR.value, status_code=500):
        super(CustomException, self).__init__(message)
        self.status_code = status_code
