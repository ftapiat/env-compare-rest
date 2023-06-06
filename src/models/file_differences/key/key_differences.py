class KeyDifferences:
    def __init__(self, file_1: list[str], file_2: list[str]):
        self.file_1 = file_1
        self.file_2 = file_2


class KeyDifferencesGenerator:
    def __init__(self, file_1_values_list: list[dict[str, str]], file_2_values_list: list[dict[str, str]]):
        self.file_1_values_list = file_1_values_list
        self.file_2_values_list = file_2_values_list

    def generate(self):
        key = "key"  # Todo make this dynamic as a class property
        return KeyDifferences(
            get_key_differences(key, self.file_1_values_list, self.file_2_values_list),
            get_key_differences(key, self.file_2_values_list, self.file_1_values_list),
        )


def get_key_differences(key: str, file_1_values_list: list[dict[str, str]], file_2_values_list: list[dict[str, str]]):
    return [
        item[key]  # Value to keep in list
        for item in file_1_values_list  # Check the main list
        if item[key] not in [  # Will only keep the values that are not in the other list
            i[key] for i in file_2_values_list
        ]
    ]
