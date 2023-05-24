from marshmallow import Schema, fields, post_load
from ..validations import content_validation
from .get_file_values_request import GetFileValuesRequest


class GetFileValuesRequestFileSchema(Schema):
    name = fields.Str(required=True)
    content = fields.Str(required=True, validate=content_validation)


class GetFileValuesRequestSchema(Schema):
    file = fields.Nested(GetFileValuesRequestFileSchema, required=True)

    @post_load
    def make_get_file_values_request(self, data, **kwargs) -> GetFileValuesRequest:
        return GetFileValuesRequest(**data)
