import pytest
from marshmallow import fields
from src.common.enums import MarshmallowCustomValidationMessages
from src.common.exceptions import InvalidParameterException
from src.serializers.base import BaseSerializer


class TestSerializer(BaseSerializer):
    name = fields.Str(required=True)
    age = fields.Int(required=True)


def test_handle_error_missing_data():
    serializer = TestSerializer()
    with pytest.raises(InvalidParameterException) as exc_info:
        serializer.load({"age": 20})

    assert str(exc_info.value) == MarshmallowCustomValidationMessages.MISSING_DATA.value.format(field="name")


def test_handle_error_invalid_data():
    serializer = TestSerializer()
    with pytest.raises(InvalidParameterException) as exc_info:
        serializer.load({"name": "Test Name", "age": "not an integer"})
    assert str(exc_info.value) == MarshmallowCustomValidationMessages.INVALID_DATA.value.format(field="age")


def test_handle_error_generic_error():
    class GenericSerializer(BaseSerializer):
        data = fields.Str(required=True)

    serializer = GenericSerializer()
    with pytest.raises(InvalidParameterException) as exc_info:
        serializer.load({"data": None})
    assert MarshmallowCustomValidationMessages.GENERIC_ERROR.value.format(field="data") in str(exc_info.value)


def test_load_success():
    serializer = TestSerializer()
    data = {"name": "John", "age": 30}
    result = serializer.load(data)
    assert result == {"name": "John", "age": 30}


def test_load_partial_data():
    serializer = TestSerializer()
    data = {"name": "Alice"}
    result = serializer.load(data, partial=True)
    assert result == {"name": "Alice"}
