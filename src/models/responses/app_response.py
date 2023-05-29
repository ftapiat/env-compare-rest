from .app_response_status import AppResponseStatus


class AppResponse:
    def __init__(self, data, message=None, status=AppResponseStatus, service=None):
        self.data = data
        self.message = message
        self.status = status
        self.service = service
