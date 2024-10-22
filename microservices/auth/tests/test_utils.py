from flask_jwt_extended import decode_token
from src.common.utils import generate_token
from tests.conftest import mock_app
from tests.conftest import user_with_roles


def test_generate_token(mock_app, user_with_roles):
    with mock_app.app_context():
        user_auth, _ = user_with_roles
        token = generate_token(user_auth)
        decoded_token = decode_token(token)
        assert decoded_token["sub"] == user_auth.id
        assert decoded_token["role"] == "admin"

        assert "read" in decoded_token["permissions"]
        assert "write" in decoded_token["permissions"]
        assert "delete" in decoded_token["permissions"]
