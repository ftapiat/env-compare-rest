from marshmallow import Schema, fields, validate
from src.models.file_types import FileTypeName
from .validations import content_validation


class IsFileTypeRequest(Schema):
    content = fields.Str(required=True, validate=content_validation)
    type_name = fields.Str(required=True, validate=validate.OneOf(FileTypeName.available_list()))
