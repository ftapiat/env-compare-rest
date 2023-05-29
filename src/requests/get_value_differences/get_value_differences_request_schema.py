from marshmallow import Schema, fields, post_load

from src.models.file_values import FileValuesSchema
from .get_value_differences_request import GetValueDifferencesRequest


def validate_values_length(values):
    if len(values) != 2:
        raise ValueError("Values must be a list of 2 elements")


class GetValueDifferencesRequestSchema(Schema):
    values = fields.List(fields.Nested(FileValuesSchema), required=True, validate=validate_values_length)

    @post_load
    def make_get_values_differences_request(self, data, **kwargs) -> GetValueDifferencesRequest:
        return GetValueDifferencesRequest(**data)
