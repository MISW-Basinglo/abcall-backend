from marshmallow import fields
from marshmallow import Schema
from marshmallow.validate import Length
from src.common.exceptions import InvalidParameterException
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import Column
from sqlalchemy import DateTime


class CompanyInputSerializer(Schema):
    name = fields.String(required=True, validate=Length(min=1, max=500))
    nit = fields.String(required=True, validate=Length(min=1, max=50))
    plan = fields.String(required=True, validate=Length(min=1, max=120))
    status = fields.String(required=True, validate=Length(min=1, max=100))
    created_at = Column(DateTime(), nullable=True, default=func.now())  # Se crea automáticamente
    updated_at = Column(DateTime(), nullable=True, default=func.now(), onupdate=func.now())  # Se actualiza automáticamente

    def load_with_exception(self, data):
        try:
            return self.load(data)
        except Exception as err:
            raise InvalidParameterException(f"Validation errors: {err}")

class CompanyResponseSerializer(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    nit = fields.String(required=True)
    plan = fields.String(required=True)
    status = fields.String(required=True)
    created_at = fields.DateTime(allow_none=True)
    update_at = fields.DateTime(allow_none=True)