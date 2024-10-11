import json

from flask import current_app  # noqa
from src.common.logger import logger
from src.db import SessionLocal
from src.models.auth import UserAuth
from src.models.auth import UserRoles
from src.models.permission import Permission
from src.models.permission import RolePermissions
from src.models.role import Role

FIXTURES_FILE_PATH = "src/fixtures/fixtures.json"


def register_commands(app):
    @app.cli.command("load-fixtures")
    def load_fixtures():
        """Command to load test data (fixtures) from a JSON file."""
        logger.info(f"Loading test data from {FIXTURES_FILE_PATH}...")
        with open(FIXTURES_FILE_PATH, "r") as f:
            data = json.load(f)

        session = SessionLocal()

        permissions_map = {}
        for permission_data in data["permissions"]:
            permission = session.query(Permission).filter_by(name=permission_data["name"]).first()
            if not permission:
                permission = Permission(name=permission_data["name"])
                session.add(permission)
            permissions_map[permission.name] = permission

        roles_map = {}
        for role_data in data["roles"]:
            role_permissions = [permissions_map[perm_name] for perm_name in role_data["permissions"]]

            role = session.query(Role).filter_by(name=role_data["name"]).first()
            if not role:
                role = Role(name=role_data["name"])
                session.add(role)

            session.flush()

            for permission in role_permissions:
                role_permission = session.query(RolePermissions).filter_by(role_id=role.id, permission_id=permission.id).first()
                if not role_permission:
                    role_permission = RolePermissions(role_id=role.id, permission_id=permission.id)
                    session.add(role_permission)

            roles_map[role.name] = role

        for user_data in data["users"]:
            user_roles = [roles_map[role_name] for role_name in user_data["roles"]]
            user = session.query(UserAuth).filter_by(email=user_data["email"]).first()
            if not user:
                user = UserAuth(email=user_data["email"])
                user.set_password(user_data["password"])
                session.add(user)

            session.flush()

            for role in user_roles:
                user_role = session.query(UserRoles).filter_by(user_auth_id=user.id, role_id=role.id).first()
                if not user_role:
                    user_role = UserRoles(user_auth_id=user.id, role_id=role.id)
                    session.add(user_role)

        session.commit()
        session.close()
        logger.info(f"Test data loaded successfully from {FIXTURES_FILE_PATH}.")
