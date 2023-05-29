from marshmallow import Schema, fields, post_load

from ..file_types import FileTypeName
from .file_values import FileValues


class FileValuesSchema(Schema):
    file_name = fields.Str(required=True)
    type_name = fields.Enum(FileTypeName, by_value=True, required=True)
    values = fields.List(fields.Dict(keys=fields.Str(), values=fields.Str()), required=True)

    @post_load
    def make_file_values(self, data, **kwargs):
        return FileValues(**data)
