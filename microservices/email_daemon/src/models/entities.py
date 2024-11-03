from dataclasses import dataclass

from src.common.enums import UserRoles
from src.common.enums import UserStatus


@dataclass
class AuthUser:
    id: int
    email: str
    status: str
    role: str

    def is_valid(self):
        return self.status == UserStatus.ACTIVE.value and self.role.lower() == UserRoles.USER.value.lower()


@dataclass
class User:
    id: int
    company_id: int
    auth_id: int
    name: str
    phone: str


@dataclass
class IssueEntity:
    type: str
    description: str
    source: str
    user_id: int
    company_id: int
    email: int = None
