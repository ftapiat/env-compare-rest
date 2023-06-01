from marshmallow import Schema, fields, post_load

from src.models.file_values import FileValuesSchema
from ..validations import files_length_validation
from .get_value_differences_request import GetValueDifferencesRequest


class GetValueDifferencesRequestSchema(Schema):
    values = fields.List(fields.Nested(FileValuesSchema), required=True, validate=files_length_validation)

    @post_load
    def make_get_values_differences_request(self, data, **kwargs) -> GetValueDifferencesRequest:
        return GetValueDifferencesRequest(**data)
