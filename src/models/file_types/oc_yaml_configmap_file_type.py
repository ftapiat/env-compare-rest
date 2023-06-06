import yaml
from abc import ABC

from ..file_values import FileValues
from .file_type import FileType
from .file_type_name import FileTypeName
from .helpers import get_list_values_from_yaml_content


class OcYamlConfigmapFileType(FileType, ABC):
    yaml_object_key = "data"

    def __init__(self, content: str):
        file_type = FileTypeName.OC_YAML_CONFIGMAP
        super().__init__(file_type, content)

    def is_valid(self) -> bool:
        """
        Checks if the content is a valid oc yaml configmap file.
        """
        try:
            yaml_content = yaml.load(self.content, Loader=yaml.FullLoader)
        except yaml.YAMLError:
            return False

        if yaml_content is None:
            return False

        if isinstance(yaml_content, str):
            return False

        list_values: dict[str, any] = get_list_values_from_yaml_content(yaml_content, self.yaml_object_key)

        if list_values is None:
            return False

        for key in list_values:
            # Each key should be a string
            if not isinstance(key, str):
                return False

            # Each value should be a string (or int which will be parsed later)
            value = list_values.get(key)
            if not isinstance(value, str) and not isinstance(value, int):
                return False

        return True

    def get_values(self, file_name: str) -> FileValues:
        """
        Assumes it's already a valid configmap file.
        :param file_name:
        :return: Key value pairs of the file
        """
        yaml_content = yaml.load(self.content, Loader=yaml.FullLoader)
        list_values = get_list_values_from_yaml_content(yaml_content, self.yaml_object_key)

        values = []
        for key in list_values:
            values.append({
                "key": key,
                "value": str(yaml_content.get(key))
            })

        return FileValues(file_name, self.type_name, values)
