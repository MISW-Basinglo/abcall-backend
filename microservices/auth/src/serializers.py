from marshmallow import fields
from marshmallow import Schema
from src.common.exceptions import InvalidParameterException


class UserLoginSerializer(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

    def load_with_exception(self, data):
        try:
            return self.load(data)
        except Exception as err:
            raise InvalidParameterException(f"Validation errors: {err}")


class TokenSerializer(Schema):
    access_token = fields.String()
    refresh_token = fields.String()


class AuditAuthUserSerializer(Schema):
    user_id = fields.Integer()
    role = fields.String()
    permissions = fields.List(fields.String())
