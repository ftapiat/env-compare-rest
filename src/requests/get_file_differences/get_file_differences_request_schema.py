from marshmallow import Schema, fields, post_load

from src.models.comparable_files import ComparableFileSchema
from ..validations import files_length_validation
from .get_file_differences_request import GetFileDifferencesRequest


class GetFileDifferencesRequestSchema(Schema):
    files = fields.List(fields.Nested(ComparableFileSchema), required=True, validate=files_length_validation)

    @post_load
    def make_get_values_differences_request(self, data, **kwargs) -> GetFileDifferencesRequest:
        return GetFileDifferencesRequest(**data)
