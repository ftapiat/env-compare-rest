class AppResponse:
    def __init__(self, data, message=None, status=str, service=None):
        self.data = data
        self.message = message
        self.status = status
        self.service = service
