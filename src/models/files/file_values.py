from ..file_types.file_type_enum import FileTypeEnum


class FileValues:
    def __init__(self, file_name: str, file_type: FileTypeEnum, values: list[dict[str, str]]):
        self.file_name = file_name
        self.file_type = file_type
        self.values = values
