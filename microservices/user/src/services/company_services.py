from src.common.constants import ExceptionsMessages
from src.common.exceptions import ResourceNotFoundException
from src.common.logger import logger
from src.models.entities import GenericResponseEntity
from src.models.entities import GenericResponseListEntity
from src.repositories.company_repository import CompanyRepository
from src.repositories.user_repository import UserRepository
from src.serializers.company_serializers import CompanyCreateSerializer
from src.serializers.company_serializers import CompanyListSerializer
from src.serializers.company_serializers import GenericResponseListSerializer
from src.serializers.company_serializers import GenericResponseSerializer
from src.serializers.user_serializers import UserListSerializer

serializer_company_class = CompanyListSerializer
serializer_user_class = UserListSerializer


def insert_company(company_data):
    data = CompanyCreateSerializer().load(company_data)
    company_repository = CompanyRepository()
    company_repository.set_serializer(serializer_company_class)
    company = company_repository.create(data)
    response_entity = GenericResponseEntity(data=company)
    response = GenericResponseSerializer().dump(response_entity)
    return response


def get_company_by_id(id_company: int):
    company_repository = CompanyRepository()
    company_repository.set_serializer(serializer_company_class)
    company = company_repository.get_by_field("id", id_company)
    response_entity = GenericResponseEntity(data=company)
    response = GenericResponseSerializer().dump(response_entity)
    return response


def get_company_by_user_session(user_id: int):
    user_repository = UserRepository()
    user_repository.set_serializer(serializer_user_class)
    user = user_repository.get_by_field("auth_id", user_id)

    if not user:
        logger.error(ExceptionsMessages.USER_NOT_REGISTERED.value)
        raise ResourceNotFoundException(ExceptionsMessages.USER_NOT_REGISTERED.value)

    company_repository = CompanyRepository()
    company_repository.set_serializer(serializer_company_class)
    company = company_repository.get_by_field("id", user["company_id"])

    if not company:
        logger.error(ExceptionsMessages.COMPANY_NOT_REGISTERED.value)
        raise ResourceNotFoundException(ExceptionsMessages.COMPANY_NOT_REGISTERED.value)

    response_entity = GenericResponseEntity(data=company)
    response = GenericResponseSerializer().dump(response_entity)
    return response


def get_all_companies():
    company_repository = CompanyRepository()
    company_repository.set_serializer(serializer_company_class)
    companies = company_repository.get_all()
    response_entity = GenericResponseListEntity(data=companies, count=len(companies))
    response = GenericResponseListSerializer().dump(response_entity)
    return response
