from src.models.entities import GenericResponseEntity
from src.models.entities import GenericResponseListEntity
from src.repositories.company_repository import CompanyRepository
from src.repositories.user_repository import UserRepository
from src.serializers.company_serializers import CompanyCreateSerializer
from src.serializers.company_serializers import CompanyListSerializer
from src.serializers.company_serializers import CompanyUpdateSerializer
from src.serializers.company_serializers import GenericResponseListSerializer
from src.serializers.company_serializers import GenericResponseSerializer
from src.serializers.user_serializers import UserListSerializer

serializer_company_class = CompanyListSerializer
serializer_user_class = UserListSerializer


def create_company_service(company_data):
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
    company_repository = CompanyRepository()
    company_repository.set_serializer(serializer_company_class)
    company = company_repository.get_by_field("id", user["company_id"])
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


def update_company_service(id_company: int, company_data):
    data = CompanyUpdateSerializer().load(company_data)
    company_repository = CompanyRepository()
    company_repository.set_serializer(serializer_company_class)
    company = company_repository.update(id_company, data)
    response_entity = GenericResponseEntity(data=company)
    response = GenericResponseSerializer().dump(response_entity)
    return response


def delete_company_service(id_company: int):
    company_repository = CompanyRepository()
    company_repository.delete(id_company)
