from typing import Optional, Generic, TypeVar

from .app_response_status import AppResponseStatus

T = TypeVar("T")


class AppResponse(Generic[T]):
    def __init__(self, data: T, status: AppResponseStatus, message: Optional[str] = None, service: Optional[str] = None):
        self.data = data
        self.status = status
        self.message = message
        self.service = service
