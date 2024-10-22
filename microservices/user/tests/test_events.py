from datetime import datetime
from datetime import timedelta
from datetime import timezone
from unittest import mock

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base
from src.events import set_utc_timestamps

# Clase de ejemplo para probar la función
Base = declarative_base()


class ExampleModel(Base):
    __tablename__ = "example_model"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)


def test_set_utc_timestamps():
    # Crear un objeto de ejemplo con fechas sin zona horaria
    naive_datetime = datetime(2024, 10, 15, 12, 0, 0)  # Sin zona horaria (naive)
    aware_datetime = datetime(2024, 10, 15, 12, 0, 0, tzinfo=timezone(timedelta(hours=-5)))  # Con zona horaria

    example_model = ExampleModel(created_at=naive_datetime, updated_at=aware_datetime)

    # Simular el mapper y la conexión que se pasan a la función (no son necesarios para esta prueba)
    mock_mapper = mock.Mock()
    mock_connection = mock.Mock()

    # Llamar a la función que queremos probar
    set_utc_timestamps(mock_mapper, mock_connection, example_model)

    # Verificar que la columna `created_at` haya sido convertida a UTC
    assert example_model.created_at.tzinfo == timezone.utc
    assert example_model.created_at == naive_datetime.replace(tzinfo=timezone.utc)

    # Verificar que la columna `updated_at` haya sido convertida de su zona horaria a UTC
    assert example_model.updated_at.tzinfo == timezone.utc
    assert example_model.updated_at == aware_datetime.astimezone(timezone.utc)
