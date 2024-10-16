from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CompanyResponseEntity:
    id: int
    name: str
    nit: str
    plan: str
    status: str
    created_at: Optional[datetime] = None
    update_at: Optional[datetime] = None
