import pytest
from src.common.enums import MarshmallowCustomValidationMessages
from src.common.exceptions import InvalidParameterException
from src.common.logger import logger
from src.serializers.company_serializers import CompanyCreateSerializer
from src.serializers.company_serializers import GenericResponseSerializer


# Test para CompanyCreateSerializer
def test_company_create_serializer_success():
    serializer = CompanyCreateSerializer()
    data = {"name": "Tech Company", "nit": "123456789", "plan": "Premium", "status": "active"}

    result = serializer.load(data)
    assert result["name"] == "Tech Company"
    assert result["nit"] == "123456789"
    assert result["plan"] == "Premium"
    assert result["status"] == "active"


def test_company_create_serializer_missing_required_fields():
    serializer = CompanyCreateSerializer()

    # Falta el campo requerido "name"
    with pytest.raises(InvalidParameterException) as exc_info:
        serializer.load({"nit": "123456789", "plan": "Premium", "status": "active"})

    logger.info("test: " + str(exc_info.value))  # Asegúrate de convertir a str para que funcione correctamente
    assert "Missing" in exc_info.value.args[0]


def test_company_create_serializer_invalid_length():
    serializer = CompanyCreateSerializer()

    # Campo "name" demasiado largo (501 caracteres)
    with pytest.raises(InvalidParameterException) as exc_info:
        serializer.load({"name": "a" * 501, "nit": "123456789", "plan": "Premium", "status": "active"})

    # Verificar si el mensaje personalizado se maneja correctamente
    expected_message = MarshmallowCustomValidationMessages.GENERIC_ERROR.value.format(field="name")
    assert str(exc_info.value) == expected_message


# Test para GenericResponseSerializer
def test_generic_response_serializer_success():
    serializer = GenericResponseSerializer()
    data = {"data": {"name": "Tech Company", "nit": "123456789", "plan": "Premium", "status": "active"}}

    result = serializer.load(data)
    assert result["data"]["name"] == "Tech Company"
    assert result["data"]["nit"] == "123456789"
    assert result["data"]["plan"] == "Premium"
    assert result["data"]["status"] == "active"
