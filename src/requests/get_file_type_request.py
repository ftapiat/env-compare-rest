from marshmallow import Schema, fields, validates, ValidationError


class GetFileTypeRequest(Schema):
    content = fields.Str(required=True)

    @validates('content')
    def validate_content(self, content):
        if content.strip() == '':
            raise ValidationError('Content is required')

        if len(content) > 1000000:
            raise ValidationError('Content is too long')
