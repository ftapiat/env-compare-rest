import difflib


class ValueDifferencesContent:
    def __init__(self, string: str, index_differences: list[int]):
        """
        :param string: Value used in the line of one file.
        :param index_differences: Differences found in the value when compared to the other value
        (from the second file).
        """
        self.string = string
        self.index_differences = index_differences

    @property
    def serialized(self):
        return {
            "string": self.string,
            "index_differences": self.index_differences
        }


class ValueDifferences:
    def __init__(self, key: str, file_1: ValueDifferencesContent, file_2: ValueDifferencesContent):
        """
        Represents the differences found in values from the same key between 2 files.
        :param key:
        :param file_1:
        :param file_2:
        """
        self.key = key
        self.file_1 = file_1
        self.file_2 = file_2

    @property
    def serialized(self):
        return {
            "key": self.key,
            "file_1": self.file_1.serialized,
            "file_2": self.file_2.serialized
        }


class ValueDifferencesGenerator:
    def __init__(self, file_1_values_list: list[dict[str, str]], file_2_values_list: list[dict[str, str]]):
        self.file_1_values_list = file_1_values_list
        self.file_2_values_list = file_2_values_list

    def generate_list(self) -> list[ValueDifferences]:
        return self.__get_differences_by_keys(self.__get_similar_key_values())

    def generate_ordered_list(self) -> list[ValueDifferences]:
        ordered_keys = sorted(self.__get_similar_key_values())
        return self.__get_differences_by_keys(ordered_keys)

    def __get_similar_key_values(self) -> list[str]:
        key = "key"  # Todo make this dynamic as a class property
        return [
            item[key]
            for item in self.file_1_values_list
            if item[key] in [
                i[key] for i in self.file_2_values_list
            ]
        ]

    def __get_differences_by_keys(self, keys_to_compare: list[str]) -> list[ValueDifferences]:
        return [
            self.__get_differences_by_key(key)
            for key in keys_to_compare
        ]

    def __get_differences_by_key(self, key: str) -> ValueDifferences:
        differences = self.__get_files_differences_by_key(key)
        return ValueDifferences(key, differences["value_file_1"], differences["value_file_2"])

    def __get_files_differences_by_key(self, key: str) -> dict[str, ValueDifferencesContent]:
        value_file_1 = get_value_by_key(key, self.file_1_values_list)
        value_file_2 = get_value_by_key(key, self.file_2_values_list)
        indexes = get_index_differences(value_file_1, value_file_2)
        return {
            "value_file_1": ValueDifferencesContent(value_file_1, indexes["value_file_1"]),
            "value_file_2": ValueDifferencesContent(value_file_2, indexes["value_file_2"])
        }


def get_value_by_key(key_from_file: str, values_list: list[dict[str, str]]) -> str:
    key = "key"  # Todo make this dynamic as a class property
    result = next(item for item in values_list if item[key] == key_from_file)  # Searches the key-value pair in the list

    # Todo make "value" dynamic as a class property
    if "value" in result:
        return result["value"]

    # If it doesn't have a value, will return an empty string as default
    return ""


def get_index_differences(value_file_1, value_file_2) -> dict[str, list[int]]:
    value_file_1_indexes = []
    value_file_2_indexes = []

    i_val_1 = 0
    i_val_2 = 0

    diffs = difflib.ndiff(value_file_1, value_file_2)
    for i, s in enumerate(diffs):
        # s[0] can be a "+" and "-" If it's a difference. If it's a space, it means it's the same character
        # s[2] the current character
        verification = s[0]

        if verification == "-":
            # It'll be a diff in the value_file_1
            value_file_1_indexes.append(i_val_1)
            i_val_1 += 1
        elif verification == "+":
            # It'll be a diff in the value_file_2
            value_file_2_indexes.append(i_val_2)
            i_val_2 += 1
        else:
            # It's the same character, so it'll increment both indexes
            i_val_1 += 1
            i_val_2 += 1

    # Todo make indexes dynamic as a class property
    return {
        "value_file_1": value_file_1_indexes,
        "value_file_2": value_file_2_indexes
    }
