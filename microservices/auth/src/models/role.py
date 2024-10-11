from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from src.db import Base
from src.models.permission import Permission
from src.models.permission import RolePermissions


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    permissions = relationship(Permission, secondary=RolePermissions.__table__, backref="roles", lazy="joined")
