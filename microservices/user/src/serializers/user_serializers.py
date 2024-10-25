from marshmallow import fields
from marshmallow.validate import Length

from .base import BaseSerializer


class UserCreateSerializer(BaseSerializer):
    name = fields.String(required=True, validate=Length(min=3, max=500))
    company_id = fields.Integer(required=False, allow_none=True)
    phone = fields.String(required=False, validate=Length(min=3, max=50))
    auth_id = fields.Integer(required=True)


class UserUpdateSerializer(BaseSerializer):
    name = fields.String(required=False, validate=Length(min=3, max=500))
    phone = fields.String(required=False, validate=Length(min=5, max=50))
    email = fields.Email(required=False)
    channel = fields.String(required=False)


class ClientCreateSerializer(BaseSerializer):
    company_name = fields.String(required=True, validate=Length(min=3, max=500))
    nit = fields.String(required=True, validate=Length(min=3, max=50))
    plan = fields.String(required=True, validate=Length(min=3, max=120))
    user_name = fields.String(required=True, validate=Length(min=3, max=500))
    phone = fields.String(required=True, validate=Length(min=3, max=50))
    email = fields.String(required=True, validate=Length(min=3, max=50))


class UserListSerializer(UserCreateSerializer):
    id = fields.Integer()
    company_id = fields.Integer()
    created_at = fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ")
    updated_at = fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ")
    email = fields.String(required=False, allow_none=True)
    channel = fields.String(required=False, allow_none=True)
    importance = fields.Integer(required=False, allow_none=True)
    dni = fields.String(required=False, allow_none=True)


class GenericResponseListSerializer(BaseSerializer):
    count = fields.Integer()
    data = fields.List(fields.Dict())


class GenericResponseSerializer(BaseSerializer):
    data = fields.Dict()


class UserEntitySerializer(BaseSerializer):
    id = fields.Integer()
    name = fields.String()
    company_id = fields.Integer()
    email = fields.String(required=False, allow_none=True)


class UserRetrieveSerializer(BaseSerializer):
    id = fields.Integer()
    email = fields.Email(required=True)
    status = fields.String(required=True)
    role = fields.String(required=False, allow_none=True)
