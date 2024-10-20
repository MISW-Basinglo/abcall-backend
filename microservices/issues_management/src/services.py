from src.models.entities import GenericResponseListEntity
from src.repositories.issues_repository import IssuesManagementRepository
from src.serializers.serializers import GenericResponseListSerializer
from src.serializers.serializers import IssueListSerializer


def get_all_issues():
    serializer_class = IssueListSerializer
    issue_repository = IssuesManagementRepository()
    issue_repository.set_serializer(serializer_class)
    issues = issue_repository.get_all()
    response_entity = GenericResponseListEntity(data=issues, count=len(issues))
    response = GenericResponseListSerializer().dump(response_entity)
    return response
