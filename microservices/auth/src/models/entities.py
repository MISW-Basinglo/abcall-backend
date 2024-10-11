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
