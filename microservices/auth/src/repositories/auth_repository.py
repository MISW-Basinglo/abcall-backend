from src.models.auth import UserAuth
from src.models.role import Role
from src.repositories.base import BaseRepository


class UserAuthRepository(BaseRepository):
    model = UserAuth

    def __init__(self):
        super().__init__()

    def create(self, data):
        role = data.pop("role", None)
        role = self.session.query(Role).filter(Role.name == role).first()
        data["role_id"] = role.id
        return super().create(data)
