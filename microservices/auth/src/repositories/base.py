from abc import ABC

from sqlalchemy import exc
from src.common.enums import ExceptionsMessages
from src.common.exceptions import InvalidParameterException
from src.common.exceptions import ResourceNotFoundException
from src.common.logger import logger
from src.common.utils import format_exception_message
from src.db import SessionLocal


class BaseRepository(ABC):
    model = None
    serializer = None

    def __init__(self):
        self.session = SessionLocal()

    def get_serializer(self):
        return self.serializer() if self.serializer else None

    def set_serializer(self, serializer):
        self.serializer = serializer

    def _transaction(self, func, *args, write=False, **kwargs):
        try:
            result = func(*args, **kwargs)
            if write:
                self.session.commit()
                if result:
                    self.session.refresh(result)
            return self.get_serializer().dump(result) if self.serializer else result
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

    def update(self, instance_id, data):
        return self._transaction(self._update, instance_id, data, write=True)

    def _update(self, instance_id, data):
        instance = self._get_by_field("id", instance_id)
        if not instance:
            logger.error(f"{self.model.__name__} not found")
            raise ResourceNotFoundException(ExceptionsMessages.RESOURCE_NOT_FOUND.value)
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
