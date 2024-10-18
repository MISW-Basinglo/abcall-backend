from marshmallow import fields
from src.serializers.base import BaseSerializer


class IssueCreateSerializer(BaseSerializer):
    type = fields.String()
    description = fields.String()
    status = fields.String()
    source = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime(allow_none=True)
    user_id = fields.Integer()
    company_id = fields.Integer()


class IssueListSerializer(IssueCreateSerializer):
    id = fields.Integer()


class GenericResponseListSerializer(BaseSerializer):
    count = fields.Integer()
    data = fields.List(fields.Dict())


class GenericResponseSerializer(BaseSerializer):
    data = fields.Dict()
