from marshmallow import fields
from marshmallow import Schema


class GenericResponseSerializer(Schema):
    text = fields.String()
