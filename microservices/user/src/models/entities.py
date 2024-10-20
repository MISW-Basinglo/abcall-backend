from dataclasses import dataclass


@dataclass
class GenericResponseListEntity:
    count: int
    data: list[dict]


@dataclass
class GenericResponseEntity:
    data: dict
