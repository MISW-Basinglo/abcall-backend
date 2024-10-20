from datetime import datetime

import pytest  # noqa
from faker import Faker
from src.serializers.user_serializers import GenericResponseSerializer
from src.serializers.user_serializers import UserCreateSerializer
from src.serializers.user_serializers import UserListSerializer

fake = Faker()


def test_user_create_serializer_success():
    serializer = UserCreateSerializer()
    data = {"name": "John Doe", "nit": "123456789", "plan": "Basic", "status": "active"}

    result = serializer.load(data)
    assert result["name"] == "John Doe"
    assert result["nit"] == "123456789"
    assert result["plan"] == "Basic"
    assert result["status"] == "active"


def test_user_list_serializer_success():
    serializer = UserListSerializer()
    now = datetime.utcnow()

    data = {"id": 1, "name": "Alice", "company_id": 101, "nit": "987654321", "plan": "Premium", "status": "active"}

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
