import pytest
from src.common.exceptions import InvalidParameterException
from src.serializers.product_serializers import (
    ProductUserListSerializer,
    ProductUserCreateSerializer,
    ProductListSerializer,
    GenericResponseListSerializer,
    GenericResponseSerializer
)


# Test para ProductUserCreateSerializer
def test_product_user_create_serializer_success():
    serializer = ProductUserCreateSerializer()
    data = {"id_user": 1, "product_id": 100}

    result = serializer.load(data)
    assert result["id_user"] == 1
    assert result["product_id"] == 100


# Test para ProductUserListSerializer
def test_product_user_list_serializer_success():
    serializer = ProductUserListSerializer()
    data = {"id": 1, "id_user": 1, "product_id": 100}

    result = serializer.load(data)
    assert result["id"] == 1
    assert result["id_user"] == 1
    assert result["product_id"] == 100


# Test para ProductListSerializer
def test_product_list_serializer_success():
    serializer = ProductListSerializer()
    data = {
        "id": 1,
        "company_id": 123,
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z",
        "type": "Software",
        "description": "Product description",
        "status": "active"
    }

    result = serializer.load(data)
    assert result["id"] == 1
    assert result["company_id"] == 123
    assert result["type"] == "Software"
    assert result["description"] == "Product description"
    assert result["status"] == "active"


# Test para GenericResponseListSerializer
def test_generic_response_list_serializer_success():
    serializer = GenericResponseListSerializer()
    data = {
        "count": 3,
        "data": [
            {"id": 1, "name": "Product A"},
            {"id": 2, "name": "Product B"},
            {"id": 3, "name": "Product C"}
        ]
    }

    result = serializer.load(data)
    assert result["count"] == 3
    assert len(result["data"]) == 3
    assert result["data"][0]["name"] == "Product A"


# Test para GenericResponseSerializer
def test_generic_response_serializer_success():
    serializer = GenericResponseSerializer()
    data = {"data": {"id": 1, "name": "Product A"}}

    result = serializer.load(data)
    assert result["data"]["id"] == 1
    assert result["data"]["name"] == "Product A"
