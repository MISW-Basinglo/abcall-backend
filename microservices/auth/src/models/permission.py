from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from src.db import Base


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)


class RolePermissions(Base):
    __tablename__ = "role_permissions"
    role_id = Column(Integer(), ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer(), ForeignKey("permissions.id"), primary_key=True)
