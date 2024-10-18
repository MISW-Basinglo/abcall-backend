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


class IssueListSerializer(IssueCreateSerializer):
    id = fields.Integer()


class GenericResponseListSerializer(BaseSerializer):
    count = fields.Integer()
    data = fields.List(fields.Dict())


class GenericResponseSerializer(BaseSerializer):
    data = fields.Dict()
