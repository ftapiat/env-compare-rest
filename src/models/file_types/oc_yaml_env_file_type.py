import yaml
from abc import ABC

from ..file_values import FileValues
from .file_type_name import FileTypeName
from .file_type import FileType
from .helpers import get_list_values_from_yaml_content


def openshift_list_has_valid_structure(values: list) -> bool:
    """
    Check if each value in list has the property "name"
    :param values:
    :return:
    """
    for value in values:
        if "name" not in value:
            return False

    return True


def format_openshift_value_structure(value: dict) -> dict[str, str]:
    if "value" not in value:
        value["value"] = ""
    else:
        value["value"] = str(value["value"])

    return {
        "key": value["name"],
        "value": value["value"]
    }


def openshift_get_values_from_list(values: list) -> list[dict[str, str]]:
    """
    Get the values from a list of objects.
    :param values:
    :return:
    """
    result = []
    for value in values:
        result.append(format_openshift_value_structure(value))
    return result


class OcYamlEnvFileType(FileType, ABC):
    yaml_object_key = "env"

    def __init__(self, content: str):
        file_type = FileTypeName.OC_YAML_ENV
        super().__init__(file_type, content)

    def is_valid(self) -> bool:
        """
        Checks if the content is a valid oc yaml env obj file.
        """
        try:
            yaml_content = yaml.load(self.content, Loader=yaml.FullLoader)
        except yaml.YAMLError:
            return False

        if yaml_content is None:
            return False

        list_values = get_list_values_from_yaml_content(yaml_content, self.yaml_object_key)

        if list_values is None:
            return False

        return openshift_list_has_valid_structure(list_values)

    def get_values(self, file_name: str) -> FileValues:
        """
        Assumes it's already a valid oc yaml env obj file and returns the values.
        :param file_name:
        :return:
        """
        yaml_content = yaml.load(self.content, Loader=yaml.FullLoader)
        list_values = get_list_values_from_yaml_content(yaml_content, self.yaml_object_key)
        values = openshift_get_values_from_list(list_values)
        return FileValues(file_name, self.type_name, values)
