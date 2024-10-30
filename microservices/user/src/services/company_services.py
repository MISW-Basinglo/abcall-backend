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
    company = populate_company(company)
    response_entity = GenericResponseEntity(data=company)
    response = GenericResponseSerializer().dump(response_entity)
    return response


def populate_company(company) -> dict:
    user_repository = UserRepository()
    user_repository.set_serializer(serializer_user_class)
    responsible = user_repository.get_responsible_by_company(company["id"])
    company["responsible_name"] = responsible["name"]
    company["responsible_email"] = responsible["email"]
    company["responsible_phone"] = responsible["phone"]
    company["responsible_dni"] = responsible["dni"]
    return company


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

def get_users_by_company_session(user_id: int):

    user_repository = UserRepository()
    user_repository.set_serializer(serializer_user_class)
    user = user_repository.get_by_field("auth_id", user_id)

    filter_dict = {
            'company_id': ('eq', user["company_id"]),
            'importance': ('gt', 0)
        }
    users_clients = user_repository.get_by_query(filter_dict)
    response_entity = GenericResponseListEntity(data=users_clients, count=len(users_clients))
    response = GenericResponseListSerializer().dump(response_entity)
    return response

def delete_company_service(id_company: int):
    company_repository = CompanyRepository()
    company_repository.delete(id_company)
