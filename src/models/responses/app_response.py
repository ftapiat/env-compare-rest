from .app_response_status import AppResponseStatus


class AppResponse(object):
    def __init__(self, data, message=None, status_code=200, service=None):
        self.data = data
        self.message = message
        self.status = AppResponseStatus.from_status_code(status_code)
        self.service = service

    @property
    def serialized(self):
        return {
            "data": self.data,
            "message": self.message,
            "status": self.status.value,
            "service": self.service
        }
