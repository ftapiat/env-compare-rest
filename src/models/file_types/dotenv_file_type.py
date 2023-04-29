import re
from ..file_values import FileValues
from .file_type_enum import FileTypeEnum


def get_non_empty_lines(values: list[str]) -> list[{int: str}]:
    """
    Will remove empty lines or lines that are comments.
    Also, will add the number of the line with value.
    """
    non_empty = []
    for index, value in enumerate(values):
        if value.strip() != "" and not is_line_a_comment(value):
            non_empty.append({
                "index": index,
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


class DotenvFileType:
    def __init__(self, content):
        self.type = FileTypeEnum.DOTENV
        self.content = content

    def is_valid(self) -> bool:
        """
        Checks if the content is a valid dotenv file.
        """
        # Split each value in string by new line
        content = self.content.split("\n")
        lines = get_non_empty_lines(content)
        # Iterate over each line and check if it is a key value pair
        # If it is not, return false
        for line in lines:
            if not is_line_a_key_value_pair(line["value"]):
                return False

        # At this point, all lines are key value pairs
        return True

    def get_values(self) -> FileValues:
        pass
