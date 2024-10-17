from src.models.auth import UserAuth
from src.repositories.base import BaseRepository


class UserAuthRepository(BaseRepository):
    model = UserAuth

    def __init__(self):
        super().__init__()

    def delete(self, instance_id):
        raise NotImplementedError("Delete method is not allowed for UserAuthRepository")
