from marshmallow import fields
from src.serializers.base import BaseSerializer


class UserLoginSerializer(BaseSerializer):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UserRetrieveSerializer(BaseSerializer):
    id = fields.Integer()
    email = fields.Email(required=True)
    status = fields.String(required=True)
    role = fields.Method("get_role")

    def get_role(self, obj):
        return obj.role.name if obj.role else None


class UserCreateSerializer(BaseSerializer):
    email = fields.Email(required=True)
    password = fields.String(required=False, allow_none=True)
    status = fields.String(required=True)
    role = fields.String(required=False, allow_none=True)


class UserAuthUpdateSerializer(BaseSerializer):
    email = fields.Email(required=False)
    status = fields.String(required=False)


class TokenSerializer(BaseSerializer):
    access_token = fields.String()
    refresh_token = fields.String()


class AuditAuthUserSerializer(BaseSerializer):
    user_id = fields.Integer()
    role = fields.String()
    permissions = fields.List(fields.String())
    email = fields.Email()


class GenericResponseSerializer(BaseSerializer):
    data = fields.Dict()
