from typing import Dict

from flask_jwt_extended import get_jwt_identity
from src.common.enums import CompanyStatus
from src.common.logger import logger
from src.common.utils import get_request_url
from src.common.utils import send_request
from src.models.entities import GenericResponseEntity
from src.repositories.user_repository import UserRepository
from src.serializers.company_serializers import CompanyListSerializer
from src.serializers.company_serializers import GenericResponseSerializer
from src.serializers.user_serializers import ClientCreateSerializer
from src.serializers.user_serializers import UserCreateSerializer
from src.serializers.user_serializers import UserListSerializer
from src.serializers.user_serializers import UserRetrieveSerializer
from src.serializers.user_serializers import UserUpdateSerializer
from src.services.company_services import create_company_service
from src.services.company_services import delete_company_service

serializer_company_class = CompanyListSerializer
serializer_user_class = UserListSerializer


def create_client_service(client_data):
    company, auth_user, user = None, None, None
    try:
        data = ClientCreateSerializer().load(client_data)
        auth_data = {"email": data["email"], "role": "client"}
        company_data = {
            "name": data["company_name"],
            "nit": data["nit"],
            "plan": data["plan"],
            "status": CompanyStatus.ACTIVE.value,
        }
        company = create_company_service(company_data)["data"]
        url = get_request_url("auth")
        auth_user = send_request("POST", url, auth_data)["data"]
        user_data = {
            "name": data["user_name"],
            "phone": data["phone"],
            "company_id": company["id"],
            "auth_id": auth_user["id"],
        }
        user = create_user_service(user_data)
        response_entity = GenericResponseEntity(data=data)
        response = GenericResponseSerializer().dump(response_entity)
        return response
    except Exception as e:
        logger.error(f"Error creating client: {e}")
        logger.info("Rolling back transactions.")
        if user:
            delete_user_service(user["id"])
            logger.info(f"User {user['id']} deleted")
        if company:
            delete_company_service(company["id"])
            logger.info(f"Company {company['id']} deleted")
        if auth_user:
            delete_auth_user_service(auth_user["id"])
        raise


def create_user_service(user_data) -> Dict:
    data = UserCreateSerializer().load(user_data)
    user_repository = UserRepository()
    user_repository.set_serializer(serializer_user_class)
    user = user_repository.create(data)
    return user


def update_user_service(user_id, data):
    data = UserUpdateSerializer().load(data)
    auth_data = {"email": data["email"]}
    auth_id = get_jwt_identity()
    update_auth_user_service(auth_id, auth_data)
    user_repository = UserRepository()
    user_repository.set_serializer(serializer_user_class)
    user = user_repository.update(user_id, data, validate_self=True)
    response_entity = GenericResponseEntity(data=user)
    response = GenericResponseSerializer().dump(response_entity)
    return response


def get_user_by_field_service(params: list):
    user_repository = UserRepository()
    user_repository.set_serializer(serializer_user_class)
    user = user_repository.get_by_field(*params)
    auth_data = user_repository.get_auth_user_data_service(user["auth_id"])
    auth_data.pop("id", None)
    user.pop("auth_id", None)
    user.update(auth_data)
    response_entity = GenericResponseEntity(data=user)
    response = GenericResponseSerializer().dump(response_entity)
    return response


def update_auth_user_service(auth_id: int, data: dict):
    url = get_request_url("auth")
    response = send_request("PUT", f"{url}/{auth_id}", data)["data"]
    return UserRetrieveSerializer().load(response)


def delete_user_service(id_user: int):
    user_repository = UserRepository()
    user_repository.delete(id_user)


def delete_auth_user_service(id_auth_user: int):
    url = get_request_url("auth")
    send_request("DELETE", f"{url}/{id_auth_user}")
