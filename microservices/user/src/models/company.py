# app/models.py
from email.policy import default

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.common.enums import CompanyPlan
from src.common.enums import CompanyStatus
from src.db import Base


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer(), primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    nit = Column(String(120), unique=True, nullable=False)
    plan = Column(SQLAlchemyEnum(CompanyPlan), unique=False, nullable=False)
    status = Column(SQLAlchemyEnum(CompanyStatus), unique=False, nullable=False, default=CompanyStatus.ACTIVE)
    created_at = Column(DateTime(), nullable=False, default=func.now())
    updated_at = Column(DateTime(), nullable=False, default=func.now(), onupdate=func.now())
    users = relationship("User", back_populates="company")
