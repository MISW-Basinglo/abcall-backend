from src.models.auth import UserAuth
from src.repositories.base import BaseRepository


class UserAuthRepository(BaseRepository):
    model = UserAuth

    def __init__(self):
        super().__init__()
