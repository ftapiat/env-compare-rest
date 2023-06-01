from marshmallow import Schema, fields, post_load

from .value_differences import ValueDifferences, ValueDifferencesContent


class ValueDifferencesContentSchema(Schema):
    string = fields.Str(required=True)
    index_differences = fields.List(fields.Int(), required=True)

    @post_load
    def make_file_differences_content(self, data, **kwargs) -> ValueDifferencesContent:
        return ValueDifferencesContent(**data)


class ValueDifferencesSchema(Schema):
    key = fields.Str(required=True)
    file_1 = fields.Nested(ValueDifferencesContentSchema, required=True)
    file_2 = fields.Nested(ValueDifferencesContentSchema, required=True)

    @post_load
    def make_file_differences(self, data, **kwargs) -> ValueDifferences:
        return ValueDifferences(**data)
