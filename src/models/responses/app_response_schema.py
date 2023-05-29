from marshmallow import Schema, fields, post_load

from .app_response_status import AppResponseStatus
from .app_response import AppResponse


class AppResponseSchema(Schema):
    data = fields.Raw(allow_none=True)
    message = fields.Str(allow_none=True)
    status_code = fields.Int()
    service = fields.Str(allow_none=True)
    status = fields.Enum(AppResponseStatus, allow_none=True, by_value=True)

    @post_load
    def make_app_response(self, data, **kwargs) -> AppResponse:
        if "status_code" in data:
            data["status"] = AppResponseStatus.from_status_code(data["status_code"])
            del data["status_code"]

        return AppResponse(**data)
