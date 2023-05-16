from marshmallow import Schema, fields, validate
from src.models.file_types import FileTypeName


class IsFileTypeRequest(Schema):
    content = fields.Str(required=True)
    type_name = fields.Str(required=True, validate=validate.OneOf(FileTypeName.available_list()))
