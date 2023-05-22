from marshmallow import Schema, fields, post_load
from .app_response_status import AppResponseStatus


class AppResponse(Schema):
    data = fields.Raw(allow_none=True)
    message = fields.Str(allow_none=True)
    status_code = fields.Int()
    status = fields.Str()
    service = fields.Str(allow_none=True)

    @post_load
    def add_status(self, data, **kwargs):
        data["status"] = AppResponseStatus.from_status_code(data["status_code"]).value
        return data
