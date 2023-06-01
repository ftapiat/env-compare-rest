from marshmallow import Schema, post_load, fields

from src.models.file_values import FileValuesSchema
from src.models.comparer import ComparedValuesSchema
from .get_file_values_response import GetFileValuesResponseValues, GetFileValuesResponse


class GetFileValuesResponseValuesSchema(Schema):
    file_1 = fields.Nested(FileValuesSchema, required=True)
    file_2 = fields.Nested(FileValuesSchema, required=True)

    @post_load
    def make_get_file_values_response_values(self, data, **kwargs):
        return GetFileValuesResponseValues(**data)


class GetFileValuesResponseSchema(Schema):
    values = fields.Nested(GetFileValuesResponseValuesSchema, required=True)
    differences = fields.Nested(ComparedValuesSchema, required=True)

    @post_load
    def make_get_file_values_response(self, data, **kwargs):
        return GetFileValuesResponse(**data)
