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
from src.common.enums import ProductStatus
from src.common.enums import TypeProduct
from src.db import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer(), primary_key=True)
    type = Column(SQLAlchemyEnum(TypeProduct), unique=False, nullable=False, default=TypeProduct.PRODUCT)
    description = Column(String(120), unique=False, nullable=False)
    status = Column(SQLAlchemyEnum(ProductStatus), unique=False, nullable=False, default=ProductStatus.ACTIVE)
    company_id = Column(Integer(), ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime(), nullable=True, default=func.now())
    updated_at = Column(DateTime(), nullable=True, default=func.now(), onupdate=func.now())
