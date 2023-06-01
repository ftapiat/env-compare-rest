from src.models.file_values import FileValues


class GetValueDifferencesRequest:
    def __init__(self, values: list[FileValues]):
        self.values = values

    @property
    def file_1(self):
        return self.values[0]

    @property
    def file_2(self):
        return self.values[1]
