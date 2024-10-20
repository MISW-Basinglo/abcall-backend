# app/models.py
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from src.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    name = Column(String(120), unique=False, nullable=False)
    dni = Column(String(120), unique=True, nullable=False)
    phone = Column(String(120), unique=False, nullable=False)
    channel = Column(String(50), unique=False, nullable=False)
    auth_id = Column(Integer(), nullable=False)
    importance = Column(Integer(), nullable=False)
    company_id = Column(Integer(), ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime(), nullable=True)
    update_at = Column(DateTime(), nullable=True)
    company = relationship("Company", back_populates="users")
