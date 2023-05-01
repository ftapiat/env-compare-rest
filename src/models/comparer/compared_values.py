from ..file_values import FileValues
from ..file_differences import KeyDifferences, KeyDifferencesGenerator, ValueDifferences, ValueDifferencesGenerator

class ComparedValues:
    def __init__(self, key_differences: KeyDifferences, value_differences: list[ValueDifferences]):
        self.key_differences = key_differences
        self.value_differences = value_differences

    @property
    def serialized(self):
        return {
            "key_differences": self.key_differences.serialized,
            "value_differences": [value_differences.serialized for value_differences in self.value_differences]
        }

    @staticmethod
    def from_files(file_1_values: FileValues, file_2_values: FileValues) -> "ComparedValues":
        key_differences = KeyDifferencesGenerator(file_1_values.values, file_2_values.values).generate()
        value_differences = ValueDifferencesGenerator(file_1_values.values, file_2_values.values).generate_ordered_list()
        return ComparedValues(key_differences, value_differences)
