from src.models.file_values import FileValues


class GetValueDifferencesRequest:
    def __init__(self, values: list[FileValues]):
        self.file_1 = values[0]
        self.file_2 = values[1]
