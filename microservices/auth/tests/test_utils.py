from flask_jwt_extended import decode_token
from src.common.utils import generate_token
from tests.conftest import mock_app
from tests.conftest import user_with_roles


# Test for `generate_token`
def test_generate_token(mock_app, user_with_roles):
    with mock_app.app_context():
        # Unpack the user and password from the fixture
        user, _ = user_with_roles

        # Generate a token for the user
        token = generate_token(user)

        # Decode the token to validate its content
        decoded_token = decode_token(token)

        # Assert that the token contains the correct user ID
        assert decoded_token["sub"] == user.id

        # Assert that the token contains the correct role
        assert decoded_token["role"] == "admin"

        # Assert that the token contains the correct permissions
        assert "read" in decoded_token["permissions"]
        assert "write" in decoded_token["permissions"]
        assert "delete" in decoded_token["permissions"]
