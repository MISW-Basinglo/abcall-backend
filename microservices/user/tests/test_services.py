import pytest
from pytest_mock import mocker  # noqa
from src.common.constants import ExceptionsMessages
from src.common.exceptions import ResourceNotFoundException

import pytest
from src.models.company import Company
from src.models.user import User

from src.services import insert_company
from src.services import get_company_by_id
from src.services import get_all_companies
from src.services import get_model_company_by_id
from src.services import get_all_models_companies
from src.services import insert_company_model
from src.services import get_model_user_by_id

from .conftest import mock_company_data, mock_company, mock_user


def test_insert_company_success(mock_app, mocker, mock_company_data):
    with mock_app.app_context():
        mock_load_with_exception = mocker.patch("src.serializers.CompanyInputSerializer.load_with_exception")
        mock_add_company = mocker.patch("src.services.insert_company_model")
        
        mock_load_with_exception.return_value = mock_company_data
        mock_add_company.return_value = mock_company
        
        result = insert_company(mock_company_data)
        
        assert result == mock_company  # Asegúrate de que sea lo esperado
        mock_load_with_exception.assert_called_once_with(mock_company_data)
        mock_add_company.assert_called_once_with(mock_company_data)



def test_get_company_by_id_success(mock_app, mocker, mock_company):
    with mock_app.app_context():
        mock_get_model_company_by_id = mocker.patch("src.services.get_model_company_by_id")
        mock_serialize = mocker.patch("src.serializers.CompanyResponseSerializer.dump")
        
        mock_get_model_company_by_id.return_value = mock_company
        mock_serialize.return_value = {"id": mock_company.id, "name": mock_company.name}
        
        result = get_company_by_id(1)
        
        assert result["id"] == mock_company.id
        assert result["name"] == mock_company.name
        mock_get_model_company_by_id.assert_called_once_with(1)
        mock_serialize.assert_called_once_with(mock_company)



def test_get_company_by_id_not_found(mock_app, mocker):
    with mock_app.app_context():
        mock_get_model_company_by_id = mocker.patch("src.services.get_model_company_by_id")
        mock_get_model_company_by_id.return_value = None
        
        with pytest.raises(ResourceNotFoundException) as excinfo:
            get_company_by_id(999)
        
        assert str(excinfo.value) == ExceptionsMessages.COMPANY_NOT_REGISTERED.value


def test_get_all_companies_success(mock_app, mocker, mock_company):
    with mock_app.app_context():
        mock_get_all_models_companies = mocker.patch("src.services.get_all_models_companies")
        mock_serialize = mocker.patch("src.serializers.CompanyResponseSerializer.dump")
        
        mock_get_all_models_companies.return_value = [mock_company]
        mock_serialize.return_value = [{"id": mock_company.id, "name": mock_company.name}]
        
        result = get_all_companies()
        
        assert len(result) == 1
        assert result[0]["id"] == mock_company.id
        assert result[0]["name"] == mock_company.name
        mock_get_all_models_companies.assert_called_once()
        mock_serialize.assert_called_once_with([mock_company])



def test_get_all_companies_not_found(mock_app, mocker):
    with mock_app.app_context():
        mock_get_all_models_companies = mocker.patch("src.services.get_all_models_companies")
        mock_get_all_models_companies.return_value = []
        
        with pytest.raises(ResourceNotFoundException) as excinfo:
            get_all_companies()
        
        assert str(excinfo.value) == ExceptionsMessages.NO_COMPANIES_FOUND.value