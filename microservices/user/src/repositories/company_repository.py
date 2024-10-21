from src.models.company import Company
from src.repositories.base import BaseRepository


class CompanyRepository(BaseRepository):
    model = Company

    def __init__(self):
        super().__init__()
