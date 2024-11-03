# app/models.py
from email.policy import default

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from src.db import Base


class ProductUser(Base):
    __tablename__ = "product_user"
    id = Column(Integer(), primary_key=True)
    id_user = Column(Integer(), ForeignKey("users.id"), nullable=True)
    product_id = Column(Integer(), ForeignKey("products.id"), nullable=True)
