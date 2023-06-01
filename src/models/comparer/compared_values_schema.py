from marshmallow import Schema, fields, post_load

from ..file_differences import KeyDifferencesSchema, ValueDifferencesSchema
from .compared_values import ComparedValues


class ComparedValuesSchema(Schema):
    key_differences = fields.Nested(KeyDifferencesSchema, required=True)
    value_differences = fields.List(fields.Nested(ValueDifferencesSchema), required=True)

    @post_load
    def make_app_response(self, data, **kwargs) -> ComparedValues:
        return ComparedValues(**data)
