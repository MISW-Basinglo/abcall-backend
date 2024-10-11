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
    role_id = Column(Integer(), ForeignKey("roles.id"))

    role = relationship(Role, back_populates="users", lazy="joined")

    def set_password(self, password):
        self.password = generate_password_hash(password, method="pbkdf2")

    def get_permissions(self):
        """Get user_auth permissions"""
        permissions = set()
        for perm in self.role.permissions:
            permissions.add(perm.name)
        return list(permissions)

    def get_role(self):
        """Get user_auth roles"""
        return self.role.name

    def check_password(self, password):
        return check_password_hash(self.password, password)
