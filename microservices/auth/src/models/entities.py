from dataclasses import dataclass


@dataclass
class TokenResponseEntity:
    access_token: str
    refresh_token: str


@dataclass
class AuditAuthUser:
    user_id: int
    role: str
    permissions: list[str]


@dataclass
class GenericResponseListEntity:
    count: int
    data: list[dict]


@dataclass
class GenericResponseEntity:
    data: dict
