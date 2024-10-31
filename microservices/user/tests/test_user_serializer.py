import pytest
from faker import Faker
from src.serializers.user_serializers import (
    UserCreateSerializer,
    UserClientCreateSerializer,
    UserUpdateSerializer,
    ClientCreateSerializer,
    UserListSerializer,
    GenericResponseListSerializer,
    GenericResponseSerializer,
    UserEntitySerializer,
    UserRetrieveSerializer
)

fake = Faker()

def test_user_create_serializer_success():
    serializer = UserCreateSerializer()
    data = {
        "name": "Alice",
        "company_id": 101,
        "phone": "123456789",
        "auth_id": 1,
    }
    result = serializer.load(data)
    assert result["name"] == "Alice"
    assert result["company_id"] == 101
    assert result["phone"] == "123456789"
    assert result["auth_id"] == 1

def test_user_client_create_serializer_success():
    serializer = UserClientCreateSerializer()
    data = {
        "name": "Bob",
        "company_id": 102,
        "phone": "987654321",
        "auth_id": 2,
        "importance": 3,
        "dni": "1234567890",
        "channel": "web",
    }
    result = serializer.load(data)
    assert result["name"] == "Bob"
    assert result["company_id"] == 102
    assert result["phone"] == "987654321"
    assert result["auth_id"] == 2
    assert result["importance"] == 3
    assert result["dni"] == "1234567890"
    assert result["channel"] == "web"

def test_user_update_serializer_success():
    serializer = UserUpdateSerializer()
    data = {
        "name": "Carol",
        "phone": "123456789",
        "email": "carol@example.com",
        "channel": "sms",
    }
    result = serializer.load(data)
    assert result["name"] == "Carol"
    assert result["phone"] == "123456789"
    assert result["email"] == "carol@example.com"
    assert result["channel"] == "sms"

def test_client_create_serializer_success():
    serializer = ClientCreateSerializer()
    data = {
        "company_name": "Example Corp",
        "nit": "987654321",
        "plan": "Premium",
        "user_name": "Dave",
        "phone": "456123789",
        "email": "dave@example.com",
    }
    result = serializer.load(data)
    assert result["company_name"] == "Example Corp"
    assert result["nit"] == "987654321"
    assert result["plan"] == "Premium"
    assert result["user_name"] == "Dave"
    assert result["phone"] == "456123789"
    assert result["email"] == "dave@example.com"

def test_user_list_serializer_success():
    serializer = UserListSerializer()
    data = {
        "id": 1,
        "name": "Eve",
        "company_id": 101,
        "phone": "123456789",
        "auth_id": 1,
        "created_at": "2021-01-01T00:00:00Z",
        "updated_at": "2021-01-01T00:00:00Z",
    }
    result = serializer.load(data)
    assert result["id"] == 1
    assert result["name"] == "Eve"
    assert result["company_id"] == 101

def test_generic_response_list_serializer_success():
    serializer = GenericResponseListSerializer()
    data = {
        "count": 2,
        "data": [
            {"name": "Alice", "status": "active"},
            {"name": "Bob", "status": "inactive"}
        ]
    }
    result = serializer.load(data)
    assert result["count"] == 2
    assert result["data"][0]["name"] == "Alice"
    assert result["data"][1]["status"] == "inactive"

def test_user_entity_serializer_success():
    serializer = UserEntitySerializer()
    data = {
        "id": 1,
        "name": "Frank",
        "company_id": 101,
        "email": "frank@example.com"
    }
    result = serializer.load(data)
    assert result["id"] == 1
    assert result["name"] == "Frank"
    assert result["company_id"] == 101
    assert result["email"] == "frank@example.com"

def test_user_retrieve_serializer_success():
    serializer = UserRetrieveSerializer()
    data = {
        "id": 1,
        "email": "test@example.com",
        "status": "active",
        "role": "admin",
    }
    result = serializer.load(data)
    assert result["id"] == 1
    assert result["email"] == "test@example.com"
    assert result["status"] == "active"
    assert result["role"] == "admin"
