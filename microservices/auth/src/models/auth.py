# app/models.py
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from src.db import Base
from src.models.role import Role
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


class UserAuth(Base):
    __tablename__ = "users_auth"
    id = Column(Integer(), primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    last_login = Column(DateTime(), nullable=True)
    password = Column(String(120), nullable=False)
    roles = relationship(Role, secondary="user_roles", backref="users", lazy="joined")

    def set_password(self, password):
        self.password = generate_password_hash(password, method="pbkdf2")

    def get_permissions(self):
        """Get user_auth permissions"""
        permissions = set()
        for role in self.roles:
            for perm in role.permissions:
                permissions.add(perm.name)
        return list(permissions)

    def get_roles(self):
        """Get user_auth roles"""
        return [role.name for role in self.roles]

    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserRoles(Base):
    __tablename__ = "user_roles"
    user_auth_id = Column(Integer(), ForeignKey("users_auth.id"), primary_key=True)
    role_id = Column(Integer(), ForeignKey("roles.id"), primary_key=True)
