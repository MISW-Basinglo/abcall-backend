from src.common.constants import ExceptionsMessages
from src.common.exceptions import ResourceNotFoundException
from src.common.logger import logger
from src.models.entities import GenericResponseEntity
from src.repositories.user_repository import UserRepository
from src.serializers.company_serializers import CompanyListSerializer
from src.serializers.company_serializers import GenericResponseSerializer
from src.serializers.user_serializers import UserListSerializer

serializer_company_class = CompanyListSerializer
serializer_user_class = UserListSerializer


def get_user_session(id_user_auth: int):
    user_repository = UserRepository()
    user_repository.set_serializer(serializer_user_class)
    user = user_repository.get_by_field("auth_id", id_user_auth)

    if not user:
        logger.error(f"{ExceptionsMessages.USER_NOT_REGISTERED.value}: {id_user_auth}")
        raise ResourceNotFoundException(ExceptionsMessages.USER_NOT_REGISTERED.value)

    response_entity = GenericResponseEntity(data=user)
    response = GenericResponseSerializer().dump(response_entity)
    return response
