from ..file_types import FileTypeEnum


class FileValues:
    def __init__(self, file_name: str, file_type: FileTypeEnum, values: list[dict[str, str]]):
        """

        :param file_name: Name of the file uploaded. Could be specified by the user or the default name.
        :param file_type:
        :param values: List containing the ["KEY", "VALUE"] of an env file
        """
        self.file_name = file_name
        self.file_type = file_type
        self.values = values
