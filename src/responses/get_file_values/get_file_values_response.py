from src.models.comparer import ComparedValues
from src.models.file_values import FileValues


class GetFileValuesResponseValues:
    def __init__(self, file_1: FileValues, file_2: FileValues):
        self.file_1 = file_1
        self.file_2 = file_2


class GetFileValuesResponse:
    def __init__(self, values: GetFileValuesResponseValues, differences: ComparedValues):
        self.values = values
        self.differences = differences
