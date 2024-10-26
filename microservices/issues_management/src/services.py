from src.common.constants import BACKEND_HOST
from src.common.constants import USER_SERVICE_PATH
from src.common.enums import BasicRoles
from src.common.enums import ExceptionsMessages
from src.common.exceptions import InvalidParameterException
from src.common.utils import send_request
from src.models.entities import GenericResponseEntity
from src.models.entities import GenericResponseListEntity
from src.repositories.issues_repository import IssuesManagementRepository
from src.serializers.serializers import GenericResponseListSerializer
from src.serializers.serializers import GenericResponseSerializer
from src.serializers.serializers import IssueCreateSerializer
from src.serializers.serializers import IssueListSerializer
from src.serializers.serializers import UserEntitySerializer

serializer_class = IssueListSerializer


def get_all_issues_service():
    issue_repository = IssuesManagementRepository()
    issue_repository.set_serializer(serializer_class)
    issues = issue_repository.get_all()
    response_entity = GenericResponseListEntity(data=issues, count=len(issues))
    response = GenericResponseListSerializer().dump(response_entity)
    return response


def get_issue_service(issue_id):
    issue_repository = IssuesManagementRepository()
    issue_repository.set_serializer(serializer_class)
    issue = issue_repository.get_by_field("id", issue_id)
    response_entity = GenericResponseEntity(data=issue)
    response = GenericResponseSerializer().dump(response_entity)
    return response


def create_issue_service(data):
    dni = data.pop("dni", None)
    user = get_user_info(dni=dni)
    if user["role"] == BasicRoles.USER.value:
        data.update({"user_id": user["id"], "company_id": user["company_id"]})
        data = IssueCreateSerializer().load(data)
        issue_repository = IssuesManagementRepository()
        issue_repository.set_serializer(serializer_class)
        issue = issue_repository.create(data)
        response_entity = GenericResponseEntity(data=issue)
        response = GenericResponseSerializer().dump(response_entity)
        return response
    else:
        raise InvalidParameterException(ExceptionsMessages.USER_NOT_AUTHORIZED.value)


def get_user_info(dni) -> dict[str, str]:
    if dni:
        params = f"?dni={dni}"
    else:
        params = "?scope=me"
    url = f"{BACKEND_HOST}{USER_SERVICE_PATH}" + params
    response = send_request("GET", url)["data"]
    required_fields = ["id", "name", "company_id", "email", "role"]
    user_data = {field: response[field] for field in required_fields}
    return UserEntitySerializer().load(user_data)
