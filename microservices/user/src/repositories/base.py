from abc import ABC

from flask_jwt_extended import get_jwt_identity
from sqlalchemy import and_
from sqlalchemy import exc
from src.common.enums import ExceptionsMessages
from src.common.exceptions import InvalidParameterException
from src.common.exceptions import ResourceNotFoundException
from src.common.exceptions import UserNotAuthorizedException
from src.common.logger import logger
from src.common.utils import format_exception_message
from src.db import SessionLocal


class BaseRepository(ABC):
    model = None
    serializer = None

    def __init__(self):
        self.session = SessionLocal()

        self.operator_map = {
            "eq": lambda field, value: field == value,
            "ne": lambda field, value: field != value,
            "lt": lambda field, value: field < value,
            "gt": lambda field, value: field > value,
            "le": lambda field, value: field <= value,
            "ge": lambda field, value: field >= value,
            "in": lambda field, value: field.in_(value),
            "like": lambda field, value: field.like(value),
        }

    def get_serializer(self):
        return self.serializer() if self.serializer else None

    def set_serializer(self, serializer):
        self.serializer = serializer

    def _serialize(self, data):
        serializer = self.get_serializer()
        if serializer:
            if isinstance(data, list):
                return [serializer.dump(item) for item in data]
            return serializer.dump(data)
        return data

    def _transaction(self, func, *args, write=False, **kwargs):
        try:
            result = func(*args, **kwargs)
            if write:
                self.session.commit()
            return self._serialize(result)
        except exc.SQLAlchemyError as e:
            exception_cause = format_exception_message(e)
            logger.error(f"Error during transaction: {exception_cause}")
            raise InvalidParameterException(ExceptionsMessages.INVALID_PARAMETER.value)
        except Exception as e:
            logger.error(f"Error during transaction: {e}")
            raise
        finally:
            if write:
                self.session.rollback()
            self.session.close()

    def get_by_field(self, field_name, value):
        return self._transaction(self._get_by_field, field_name, value)

    def _get_by_field(self, field_name, value):
        if not hasattr(self.model, field_name):
            raise InvalidParameterException(ExceptionsMessages.INVALID_PARAMETER.value)
        instance = self.session.query(self.model).filter(getattr(self.model, field_name) == value).first()
        if not instance:
            raise ResourceNotFoundException(ExceptionsMessages.RESOURCE_NOT_FOUND.value)
        return instance

    def get_all(self):
        return self._transaction(self._get_all)

    def _get_all(self):
        return self.session.query(self.model).all()

    def update(self, instance_id, data, validate_self=False):
        return self._transaction(self._update, instance_id, data, write=True, validate_self=validate_self)

    def _update(self, instance_id, data, validate_self=False):
        instance = self._get_by_field("id", instance_id)
        if not instance:
            logger.error(f"{self.model.__name__} not found")
            raise ResourceNotFoundException(ExceptionsMessages.RESOURCE_NOT_FOUND.value)
        if validate_self:
            auth_id = get_jwt_identity()
            if getattr(instance, "auth_id", None) != auth_id:
                logger.error(f"User {auth_id} is not authorized to update this {self.model.__name__}")
                raise UserNotAuthorizedException(ExceptionsMessages.USER_NOT_AUTHORIZED.value)
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    def delete(self, instance_id):
        return self._transaction(self._delete, instance_id, write=True)

    def _delete(self, instance_id):
        instance = self._get_by_field("id", instance_id)
        if not instance:
            raise ResourceNotFoundException(ExceptionsMessages.RESOURCE_NOT_FOUND.value)
        self.session.delete(instance)

    def create(self, data):
        return self._transaction(self._create, data, write=True)

    def _create(self, data):
        instance = self.model(**data)
        self.session.add(instance)
        return instance

    def get_by_query(self, filter_dict):
        """
        Fetch records based on dynamic filters passed as a dictionary.

        :param filter_dict: Dictionary where keys are field names and values are tuples (operator, value)
        :return: Query result
        e.g:
        filter_dict = {
            'status': ('eq', 'resolved'),
            'source': ('in', ['call', 'email']),
            'type': ('eq', 'bug')
        }

        """
        return self._transaction(self._build_dynamic_query, filter_dict)

    def _build_dynamic_query(self, filter_dict):
        """
        Dynamically build a query with filters based on a dictionary, supporting different operators.

        :param filter_dict: A dictionary where keys are field names and values are tuples with (operator, value).
        :return: A SQLAlchemy query object.
        """
        query = self.session.query(self.model)

        filters = []
        for field_name, (operator, value) in filter_dict.items():
            if value is not None:
                try:
                    field = getattr(self.model, field_name)
                    operator_func = self.operator_map.get(operator)
                    if not operator_func:
                        raise InvalidParameterException(ExceptionsMessages.INVALID_PARAMETER.value)
                    filters.append(operator_func(field, value))
                except AttributeError:
                    raise InvalidParameterException(ExceptionsMessages.INVALID_PARAMETER.value)

        if filters:
            query = query.filter(and_(*filters))

        return query.all()
