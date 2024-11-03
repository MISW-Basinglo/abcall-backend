from dataclasses import dataclass


@dataclass
class GenericResponseListEntity:
    count: int
    data: list[dict]


@dataclass
class GenericResponseEntity:
    data: dict


@dataclass
class AuthUser:
    user_id: int
    role: str
    permissions: list[str]
    email: str

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions

    def has_permissions(self, permissions: list[str]) -> bool:
        return any(self.has_permission(permission) for permission in permissions)

    def has_role(self, role: list) -> bool:
        return self.role in role
