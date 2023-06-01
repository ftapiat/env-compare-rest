from marshmallow import Schema, fields, post_load

from .key_differences import KeyDifferences


class KeyDifferencesSchema(Schema):
    file_1 = fields.List(fields.Str(), required=True)
    file_2 = fields.List(fields.Str(), required=True)

    @post_load
    def make_key_differences(self, data, **kwargs) -> KeyDifferences:
        return KeyDifferences(**data)
