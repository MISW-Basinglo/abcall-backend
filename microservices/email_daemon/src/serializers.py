from marshmallow import fields
from marshmallow import Schema


class IssueCreateSerializer(Schema):
    type = fields.String(required=True)
    description = fields.String(required=True)
    source = fields.String(required=True)
    user_id = fields.Integer()
    company_id = fields.Integer()
    email = fields.Email()
