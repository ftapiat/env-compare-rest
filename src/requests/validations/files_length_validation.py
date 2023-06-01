from marshmallow import ValidationError


def files_length_validation(files):
    if len(files) != 2:
        raise ValidationError("Must be a list of 2 elements")
