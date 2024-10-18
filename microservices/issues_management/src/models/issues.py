# app/models.py
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import Text
from src.common.enums import IssueSource
from src.common.enums import IssueStatus
from src.common.enums import IssueType
from src.db import Base


class Issue(Base):
    __tablename__ = "issues"
    id = Column(Integer(), primary_key=True)
    type = Column(SqlEnum(IssueType), nullable=False)
    description = Column(Text(), nullable=False)
    status = Column(SqlEnum(IssueStatus), nullable=False, default=IssueStatus.OPEN.value)
    source = Column(SqlEnum(IssueSource), nullable=False)
    created_at = Column(DateTime(), nullable=False, default=func.now())
    updated_at = Column(DateTime(), nullable=True)
    user_id = Column(Integer())
    company_id = Column(Integer())
