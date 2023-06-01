from marshmallow import Schema, fields, post_load
from ..validations import content_validation
from .get_file_values_request import GetFileValuesRequest, GetFileValuesRequestFile


class GetFileValuesRequestFileSchema(Schema):
    name = fields.Str(required=True)
    content = fields.Str(required=True, validate=content_validation)

    @post_load
    def make_get_file_values_request_file(self, data, **kwargs) -> GetFileValuesRequestFile:
        return GetFileValuesRequestFile(**data)


class GetFileValuesRequestSchema(Schema):
    file = fields.Nested(GetFileValuesRequestFileSchema, required=True)

    @post_load
    def make_get_file_values_request(self, data, **kwargs) -> GetFileValuesRequest:
        return GetFileValuesRequest(**data)
