from enum import Enum


class UserStatus(Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    INACTIVE = "INACTIVE"


class UserRoles(Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    CLIENT = "CLIENT"
    AGENT = "AGENT"
