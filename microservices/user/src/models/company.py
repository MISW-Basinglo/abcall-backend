# app/models.py
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from src.db import Base
from sqlalchemy.sql import func


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer(), primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    nit = Column(String(120), unique=True, nullable=False)
    plan = Column(String(120), unique=False, nullable=False)
    status = Column(String(50), unique=False, nullable=False)
    created_at = Column(DateTime(), nullable=True, default=func.now())
    update_at = Column(DateTime(), nullable=True, default=func.now())
