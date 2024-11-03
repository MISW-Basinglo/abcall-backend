from marshmallow import fields
from marshmallow.validate import Length

from .base import BaseSerializer


class CompanyCreateSerializer(BaseSerializer):
    name = fields.String(required=True, validate=Length(min=1, max=500))
    nit = fields.String(required=True, validate=Length(min=1, max=50))
    plan = fields.String(required=True, validate=Length(min=1, max=120))
    status = fields.String(required=True, validate=Length(min=1, max=100))


class CompanyListSerializer(CompanyCreateSerializer):
    id = fields.Integer()
    created_at = fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ")
    updated_at = fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ")


class PopulatedCompanySerializer(CompanyListSerializer):
    responsible_name = fields.String()
    responsible_email = fields.Email()
    responsible_phone = fields.String()


class GenericResponseListSerializer(BaseSerializer):
    count = fields.Integer()
    data = fields.List(fields.Dict())


class GenericResponseSerializer(BaseSerializer):
    data = fields.Dict()


class CompanyUpdateSerializer(CompanyCreateSerializer):
    name = fields.String(validate=Length(min=1, max=500))
    nit = fields.String(validate=Length(min=1, max=50))
    plan = fields.String(validate=Length(min=1, max=120))
    status = fields.String(validate=Length(min=1, max=100))
