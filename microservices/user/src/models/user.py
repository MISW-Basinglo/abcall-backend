# app/models.py
from email.policy import default

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from src.common.enums import UserChannel
from src.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    name = Column(String(120), unique=False, nullable=False)
    dni = Column(String(120), unique=True, nullable=True)
    phone = Column(String(120), unique=False, nullable=False)
    channel = Column(SQLAlchemyEnum(UserChannel), nullable=True, default=UserChannel.EMAIL)
    auth_id = Column(Integer(), nullable=False)
    importance = Column(Integer(), nullable=True)
    company_id = Column(Integer(), ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime(), nullable=True, default=func.now())
    updated_at = Column(DateTime(), nullable=True, default=func.now(), onupdate=func.now())
    company = relationship("Company", back_populates="users")
