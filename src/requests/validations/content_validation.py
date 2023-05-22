from marshmallow import ValidationError


def content_validation(content):
    if content.strip() == '':
        raise ValidationError('Content is required')

    if len(content) > 1000000:
        raise ValidationError('Content is too long')
