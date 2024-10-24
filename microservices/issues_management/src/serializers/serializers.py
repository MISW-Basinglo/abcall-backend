from marshmallow import fields
from src.serializers.base import BaseSerializer


class IssueCreateSerializer(BaseSerializer):
    type = fields.String(required=True)
    description = fields.String(required=True)
    status = fields.String()
    source = fields.String(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime(allow_none=True, required=False)
    user_id = fields.Integer()
    company_id = fields.Integer()
    solution = fields.String(allow_none=True, required=False)


class IssueListSerializer(IssueCreateSerializer):
    id = fields.Integer()
    created_at = fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ")
    updated_at = fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ")


class GenericResponseListSerializer(BaseSerializer):
    count = fields.Integer()
    data = fields.List(fields.Dict())


class GenericResponseSerializer(BaseSerializer):
    data = fields.Dict()


class UserEntitySerializer(BaseSerializer):
    id = fields.Integer()
    name = fields.String()
    company_id = fields.Integer()
