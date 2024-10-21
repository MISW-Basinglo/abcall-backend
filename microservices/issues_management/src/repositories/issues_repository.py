from src.models.issues import Issue
from src.repositories.base import BaseRepository


class IssuesManagementRepository(BaseRepository):
    model = Issue

    def __init__(self):
        super().__init__()
