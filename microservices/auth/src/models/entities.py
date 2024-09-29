from dataclasses import dataclass


@dataclass
class TokenResponseEntity:
    access_token: str
    refresh_token: str
