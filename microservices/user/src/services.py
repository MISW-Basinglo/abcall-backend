from datetime import datetime
from datetime import timedelta
from typing import Dict

from src.common.constants import ExceptionsMessages
from src.common.constants import JWT_REFRESH_DELTA
from src.common.decorators import db_session
from src.common.exceptions import ResourceNotFoundException
from src.common.logger import logger
from src.models.company import Company
from src.models.user import User
from src.models.entities import CompanyResponseEntity
from src.serializers import CompanyResponseSerializer, CompanyInputSerializer


def insert_company(company_data):
    company_input = CompanyInputSerializer().load_with_exception(company_data)
    return insert_company_model(company_input)


def get_company_by_id(idCompany: int):
    # Obtener el modelo de la base de datos usando alguna función
    company_model = get_model_company_by_id(idCompany)

    # Verificar si la compañía existe
    if not company_model:
        logger.error(ExceptionsMessages.COMPANY_NOT_REGISTERED.value)
        raise ResourceNotFoundException(ExceptionsMessages.COMPANY_NOT_REGISTERED.value)
    else:
        logger.info("Compañía Existe")

    # Mapeo de company_model a CompanyResponseEntity
    company = CompanyResponseEntity(
        id=idCompany,
        name=company_model.name,
        nit=company_model.nit,
        plan=company_model.plan,
        status=company_model.status,
        created_at=company_model.created_at,
        update_at=company_model.update_at
    )

    # Serializar la respuesta
    company_serializer = CompanyResponseSerializer()
    return company_serializer.dump(company)


def get_company_by_user_session(user_id: int):
    # Obtener el modelo de la base de datos usando alguna función
    user_model = get_model_user_by_id(user_id)

    if not user_model:
        logger.error(ExceptionsMessages.USER_NOT_REGISTERED.value)
        raise ResourceNotFoundException(ExceptionsMessages.USER_NOT_REGISTERED.value)

    company_model = get_model_company_by_id(user_model.company_id)

    # Verificar si la compañía existe
    if not company_model:
        logger.error(ExceptionsMessages.COMPANY_NOT_REGISTERED.value)
        raise ResourceNotFoundException(ExceptionsMessages.COMPANY_NOT_REGISTERED.value)
    else:
        logger.info("Compañía Existe")

    # Mapeo de company_model a CompanyResponseEntity
    company = CompanyResponseEntity(
        id=company_model.id,
        name=company_model.name,
        nit=company_model.nit,
        plan=company_model.plan,
        status=company_model.status,
        created_at=company_model.created_at,
        update_at=company_model.update_at
    )

    # Serializar la respuesta
    company_serializer = CompanyResponseSerializer()
    return company_serializer.dump(company)

def get_all_companies():
    # Obtener todas las compañías de la base de datos usando alguna función
    companies_model_list = get_all_models_companies()

    # Verificar si hay compañías en la base de datos
    if not companies_model_list:
        logger.error(ExceptionsMessages.NO_COMPANIES_FOUND.value)
        raise ResourceNotFoundException(ExceptionsMessages.NO_COMPANIES_FOUND.value)
    else:
        logger.info(f"Se encontraron {len(companies_model_list)} compañías.")

    # Mapeo de cada company_model a CompanyResponseEntity
    companies = [
        CompanyResponseEntity(
            id=company_model.id,
            name=company_model.name,
            nit=company_model.nit,
            plan=company_model.plan,
            status=company_model.status,
            created_at=company_model.created_at,
            update_at=company_model.update_at
        )
        for company_model in companies_model_list
    ]

    # Serializar el listado de respuestas
    company_serializer = CompanyResponseSerializer(many=True)  # many=True para serializar una lista
    return company_serializer.dump(companies)

@db_session
def get_model_company_by_id(session, company_id):
    company = session.query(Company).filter(Company.id == company_id).first()
    return company

@db_session
def get_all_models_companies(session):
    # Consulta todas las compañías
    companies = session.query(Company).all()
    return companies

@db_session
def insert_company_model(session, new_company):
    company = Company(**new_company)
    session.add(company)
    session.commit()
    company_serializer = CompanyResponseSerializer()
    return company_serializer.dump(company)

@db_session
def get_model_user_by_id(session, user_id: int):
    user = session.query(User).filter(User.auth_id == user_id).first()
    return user