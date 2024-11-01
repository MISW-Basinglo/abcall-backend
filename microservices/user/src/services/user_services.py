from typing import Dict

from flask_jwt_extended import get_jwt_identity
from src.common.enums import CompanyStatus
from src.common.logger import logger
from src.common.utils import get_request_url
from src.common.utils import send_request
from src.models.entities import GenericResponseEntity, GenericResponseListEntity
from src.repositories.user_repository import UserRepository
from src.repositories.product_user_repository import ProductUserRepository
from src.repositories.product_repository import ProductRepository
from src.serializers.company_serializers import CompanyListSerializer
from src.serializers.company_serializers import GenericResponseSerializer
from src.serializers.user_serializers import ClientCreateSerializer
from src.serializers.user_serializers import UserCreateSerializer
from src.serializers.user_serializers import UserClientCreateSerializer
from src.serializers.user_serializers import UserListSerializer
from src.serializers.user_serializers import UserMinimalSerializer
from src.serializers.user_serializers import UserRetrieveSerializer
from src.serializers.user_serializers import UserUpdateSerializer
from src.serializers.product_serializers import ProductUserListSerializer
from src.serializers.product_serializers import ProductListSerializer
from src.serializers.product_serializers import ProductUserCreateSerializer
from src.serializers.product_serializers import GenericResponseListSerializer
from src.serializers.product_serializers import GenericResponseSerializer
from src.services.company_services import create_company_service
from src.services.company_services import delete_company_service
from src.common.enums import UserChannel

from src.common.utils import format_exception_message

from src.common.enums import ExceptionsMessages
from src.common.exceptions import CustomException

serializer_company_class = CompanyListSerializer
serializer_user_class = UserListSerializer
serializer_product_user_class = ProductUserListSerializer
serializer_product_class = ProductListSerializer


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

def imports_users_service(user_id, data):

    # Obtener idCompany del cliente en sesión
    user_repository = UserRepository()
    user_repository.set_serializer(serializer_user_class)
    user = user_repository.get_by_field("auth_id", user_id)

    
    for row in data:
        if data.line_num == 1:
            continue

        #Crear Auth de los usuarios
        auth_data = {"email": row[2], "role": "user", "password": row[3]}
        url = get_request_url("auth")
        try:
            auth_user = send_request("POST", url, auth_data)["data"]
        except Exception as e:
            logger.error(ExceptionsMessages.RESOURCE_EXISTS.value + ": " + row[2])
            raise CustomException(ExceptionsMessages.RESOURCE_EXISTS.value + " : " + row[2])
        
        user_data = {
            "name": row[0],
            "phone": row[1],
            "company_id": user["company_id"],
            "auth_id": auth_user["id"],
            "importance": int(row[4]),
            "dni": row[3],
            "channel": UserChannel.EMAIL.value
        }
        user = create_user_client_service(user_data)

        products = get_products_service(user["company_id"])

        for item in products:
            data_product_user = {
                "id_user": user["id"],
                "product_id": item["id"]
            }
            data_new_product_user = ProductUserCreateSerializer().load(data_product_user)
            
            product_user_repository = ProductUserRepository()
            product_user_repository.set_serializer(serializer_product_user_class)
            product_user_repository.create(data_new_product_user)

    data_response = {
        "msg": "Usuarios importados correctamente"
    }

    response_entity = GenericResponseEntity(data=data_response)
    response = GenericResponseSerializer().dump(response_entity)
    return response

def create_user_client_service(user_data) -> Dict:
    data = UserClientCreateSerializer().load(user_data)
    user_repository = UserRepository()
    user_repository.set_serializer(serializer_user_class)
    user = user_repository.create(data)
    return user

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


def get_minimal_user_by_field(params: list):
    user_repository = UserRepository()
    user_repository.set_serializer(UserMinimalSerializer)
    user = user_repository.get_by_field(*params)
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

def get_products_by_user_service(id_user: int):
    product_user_repository = ProductUserRepository()
    product_user_repository.set_serializer(serializer_product_user_class)
    filter_dict = {
            'id_user': ('eq', id_user)
        }
    product_user = product_user_repository.get_by_query(filter_dict)
    product_ids = list({pu['product_id'] for pu in product_user})
    filter_dict = {
            'id': ('in', product_ids)
        }

    product_repository = ProductRepository()
    product_repository.set_serializer(serializer_product_class)
    product = product_repository.get_by_query(filter_dict)
    response_entity = GenericResponseListEntity(data=product, count=len(product))
    response = GenericResponseListSerializer().dump(response_entity)
    return response


def get_products_service(id_company: int):

    filter_dict = {
                'company_id': ('eq', id_company)
        }
    product_repository = ProductRepository()
    product_repository.set_serializer(serializer_product_class)
    products = product_repository.get_by_query(filter_dict)
    return products