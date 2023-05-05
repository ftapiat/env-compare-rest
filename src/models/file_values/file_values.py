from typing import Any

from ..file_types import FileTypeName


class FileValues:
    def __init__(self, file_name: str, file_type: FileTypeName, values: list[dict[str, str]]):
        """
        Represents the values of an env file.
        :param file_name: Name of the file uploaded. Could be specified by the user or the default name.
        :param file_type:
        :param values: List containing the ["KEY", "VALUE"] of an env file
        """
        self.file_name = file_name
        self.file_type = file_type
        self.values = values

    @property
    def serialized(self):
        return {
            "file_name": self.file_name,
            "file_type": self.file_type.value,
            "values": self.values
        }

    @staticmethod
    def from_dict(data: dict[str, Any]):
        return FileValues(data["file_name"], FileTypeName(data["file_type"]), data["values"])