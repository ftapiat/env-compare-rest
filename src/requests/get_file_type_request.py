from marshmallow import Schema, fields
from .validations import content_validation


class GetFileTypeRequest(Schema):
    content = fields.Str(required=True, validate=content_validation)
