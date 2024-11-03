from marshmallow import fields
from marshmallow.validate import Length

from .base import BaseSerializer

class ProductUserListSerializer(BaseSerializer):
    id = fields.Integer()
    id_user = fields.Integer()
    product_id = fields.Integer()

class ProductUserCreateSerializer(BaseSerializer):
    id_user = fields.Integer()
    product_id = fields.Integer()

class ProductListSerializer(BaseSerializer):
    id = fields.Integer()
    company_id = fields.Integer()
    created_at = fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ")
    updated_at = fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ")
    type = fields.String(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)
    status = fields.String(required=False, allow_none=True)


class GenericResponseListSerializer(BaseSerializer):
    count = fields.Integer()
    data = fields.List(fields.Dict())


class GenericResponseSerializer(BaseSerializer):
    data = fields.Dict()
