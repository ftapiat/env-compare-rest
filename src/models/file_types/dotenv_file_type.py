import re
from typing import Any
from abc import ABC

from ..file_values import FileValues
from .file_type_name import FileTypeName
from .file_type import FileType


class DotenvFileType(FileType, ABC):
    def __init__(self, content: str):
        super().__init__(FileTypeName.DOTENV, content)
        # Split each value in string by new line
        content = content.split("\n")
        self.lines = get_non_empty_lines(content)

    def is_valid(self) -> bool:
        """
        Checks if the content is a valid dotenv file.
        """
        # Iterate over each line and check if it is a key value pair
        # If it is not, return false
        for line in self.lines:
            if not is_line_a_key_value_pair(line["value"]):
                return False

        # At this point, all lines are key value pairs
        return True

    def get_values(self, file_name: str) -> FileValues:
        """
        Assumes it's already a valid dotenv file and returns the values.
        :param file_name:
        :return: Key value pairs of the file
        """
        values = []
        for line in self.lines:
            key_value: list[str, Any] = line["value"].split("=")
            values.append({
                "key": key_value[0].strip(),
                "value": key_value[1]
            })

        return FileValues(file_name, self.type_name, values)


def get_non_empty_lines(values: list[str]) -> list[{int: str}]:
    """
    Remove empty lines or lines that are comments.
    """
    non_empty = []
    for index, value in enumerate(values):
        if value.strip() != "" and not is_line_a_comment(value):
            non_empty.append({
                "line": index + 1,  # Line number
                "value": value
            })
    return non_empty


def is_line_a_comment(line):
    """
    Check if the line is a comment.
    """
    regex_dotenv_comment = r'^\s*#'
    return re.match(regex_dotenv_comment, line)


def is_line_a_key_value_pair(line):
    """
    Check if the line is a key value pair.

    Example:
        KEY=VALUE ✅
        KEY = VALUE ✅
        KEY= ✅
        KEY ❌
        #KEY=VALUE ❌
    """
    regex_key_value_pair = r"^\w+=.*"
    return re.match(regex_key_value_pair, line)
