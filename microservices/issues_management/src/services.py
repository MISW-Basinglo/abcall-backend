from src.common.constants import BACKEND_HOST
from src.common.constants import USER_SERVICE_PATH
from src.common.utils import get_auth_header_from_request
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


def create_issue_service(data):
    user = get_user_info()
    data.update({"user_id": user["id"], "company_id": user["company_id"]})
    data = IssueCreateSerializer().load(data)
    issue_repository = IssuesManagementRepository()
    issue_repository.set_serializer(serializer_class)
    issue = issue_repository.create(data)
    response_entity = GenericResponseEntity(data=issue)
    response = GenericResponseSerializer().dump(response_entity)
    return response


def get_user_info() -> dict[str, str]:
    auth_header = get_auth_header_from_request()
    url = f"{BACKEND_HOST}{USER_SERVICE_PATH}/me"
    response = send_request(url, "GET", headers=auth_header)["data"]
    return UserEntitySerializer().load(response)
