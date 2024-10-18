from src.models.entities import GenericResponseEntity
from src.models.entities import GenericResponseListEntity
from src.repositories.issues_repository import IssuesManagementRepository
from src.serializers.serializers import GenericResponseListSerializer
from src.serializers.serializers import GenericResponseSerializer
from src.serializers.serializers import IssueCreateSerializer
from src.serializers.serializers import IssueListSerializer


def get_all_issues_service():
    serializer_class = IssueListSerializer
    issue_repository = IssuesManagementRepository()
    issue_repository.set_serializer(serializer_class)
    issues = issue_repository.get_all()
    response_entity = GenericResponseListEntity(data=issues, count=len(issues))
    response = GenericResponseListSerializer().dump(response_entity)
    return response


def create_issue_service(data):
    serializer_class = IssueListSerializer
    data = IssueCreateSerializer().load(data)
    issue_repository = IssuesManagementRepository()
    issue_repository.set_serializer(serializer_class)
    issue = issue_repository.create(data)
    response_entity = GenericResponseEntity(data=issue)
    response = GenericResponseSerializer().dump(response_entity)
    return response
