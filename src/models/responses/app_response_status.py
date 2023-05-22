from enum import Enum


class AppResponseStatus(Enum):
    OK = "ok"
    ERROR = "error"

    @classmethod
    def from_status_code(cls, status_code):
        if status_code >= 400:
            return cls.ERROR
        return cls.OK
