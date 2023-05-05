from abc import ABC, abstractmethod

from ..file_values import FileValues
from .file_type_name import FileTypeName


class FileType(ABC):
    def __init__(self, type_name: FileTypeName, content: str):
        self.type_name = type_name
        self.content = content

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Checks if the content is a valid file.
        """
        pass

    @abstractmethod
    def get_values(self, file_name: str) -> FileValues:
        """
        Assumes it's already a valid dotenv file and returns the values.
        :param file_name:
        :return: Key value pairs of the file
        """
        pass
