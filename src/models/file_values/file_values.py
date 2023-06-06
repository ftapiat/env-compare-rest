from typing import Any

from ..file_types import FileTypeName


class FileValues:
    def __init__(self, file_name: str, type_name: FileTypeName, values: list[dict[str, str]]):
        """
        Represents the values of an env file.
        :param file_name: Name of the file uploaded. Could be specified by the user or the default name.
        :param type_name:
        :param values: List containing the ["KEY", "VALUE"] of an env file
        """
        self.file_name = file_name
        self.type_name = type_name
        self.values = values
