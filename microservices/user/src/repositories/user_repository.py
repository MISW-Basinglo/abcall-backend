from src.models.user import User
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    def __init__(self):
        super().__init__()
