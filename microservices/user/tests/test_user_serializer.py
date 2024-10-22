import pytest  # noqa
from faker import Faker
from src.serializers.user_serializers import GenericResponseSerializer
from src.serializers.user_serializers import UserCreateSerializer
from src.serializers.user_serializers import UserListSerializer

fake = Faker()


def test_user_create_serializer_success():
    serializer = UserCreateSerializer()
    data = {
        "name": "Alice",
        "company_id": 101,
        "phone": "123456789",
        "auth_id": 1,
    }
    data = serializer.load(data)
    assert data["name"] == "Alice"
    assert data["company_id"] == 101
    assert data["phone"] == "123456789"
    assert data["auth_id"] == 1


def test_user_list_serializer_success():
    serializer = UserListSerializer()
    data = {
        "id": 1,
        "name": "Alice",
        "company_id": 101,
        "phone": "123456789",
        "auth_id": 1,
        "created_at": "2021-01-01T00:00:00Z",
        "updated_at": "2021-01-01T00:00:00Z",
    }

    result = serializer.load(data)
    assert result["id"] == 1
    assert result["name"] == "Alice"
    assert result["company_id"] == 101


def test_generic_response_serializer_success():
    serializer = GenericResponseSerializer()
    data = {"data": {"name": "John Doe", "company_id": 123, "status": "active"}}

    result = serializer.load(data)
    assert result["data"]["name"] == "John Doe"
    assert result["data"]["company_id"] == 123
    assert result["data"]["status"] == "active"
