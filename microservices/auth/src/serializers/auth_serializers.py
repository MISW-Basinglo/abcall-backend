from marshmallow import fields
from src.serializers.base import BaseSerializer


class UserLoginSerializer(BaseSerializer):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class TokenSerializer(BaseSerializer):
    access_token = fields.String()
    refresh_token = fields.String()


class AuditAuthUserSerializer(BaseSerializer):
    user_id = fields.Integer()
    role = fields.String()
    permissions = fields.List(fields.String())
