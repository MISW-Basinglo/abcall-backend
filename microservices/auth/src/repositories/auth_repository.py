from src.common.enums import ExceptionsMessages
from src.common.exceptions import ResourceNotFoundException
from src.models.auth import UserAuth
from src.models.role import Role
from src.repositories.base import BaseRepository


class UserAuthRepository(BaseRepository):
    model = UserAuth

    def __init__(self):
        super().__init__()

    def create(self, data):
        role = self.get_role(data.pop("role", None))
        if not role:
            raise ResourceNotFoundException(ExceptionsMessages.RESOURCE_NOT_FOUND.value)
        data["role_id"] = role
        return super().create(data)

    def get_role(self, role):
        role = self.session.query(Role).filter(Role.name == role).first()
        return role.id
