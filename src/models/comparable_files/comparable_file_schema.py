from marshmallow import Schema, fields, post_load

from .comparable_file import ComparableFile


class ComparableFileSchema(Schema):
    name = fields.Str(required=True, allow_none=True)
    content = fields.Str(required=True)

    @post_load
    def make_comparable_file(self, data, **kwargs) -> ComparableFile:
        return ComparableFile(**data)
