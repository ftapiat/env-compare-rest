from abc import ABC, abstractmethod

from ..file_values import FileValues
from .file_type_enum import FileTypeEnum


class FileType(ABC):
    def __init__(self, file_type: FileTypeEnum, content: str):
        self.type = file_type
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
