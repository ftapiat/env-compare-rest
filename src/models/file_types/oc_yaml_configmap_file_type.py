import yaml
from abc import ABC

from ..file_values import FileValues
from .file_type import FileType
from .file_type_name import FileTypeName


class OcYamlConfigmapFileType(FileType, ABC):
    def __init__(self, content: str):
        file_type = FileTypeName.OC_YAML_CONFIGMAP
        super().__init__(file_type, content)

    def is_valid(self) -> bool:
        """
        Checks if the content is a valid oc yaml configmap file.
        """
        yaml_content = yaml.load(self.content, Loader=yaml.FullLoader)

        if yaml_content is None:
            return False

        for key in yaml_content:
            # Each key should be a string
            if not isinstance(key, str):
                return False

            # Each value should be a string (or int which will be parsed later)
            value = yaml_content.get(key)
            if not isinstance(value, str) and not isinstance(value, int):
                return False

        return True

    def get_values(self, file_name: str) -> FileValues:
        """
        Assumes it's already a valid configmap file.
        :param file_name:
        :return: Key value pairs of the file
        """
        yaml_content: dict[str, str] = yaml.load(self.content, Loader=yaml.FullLoader)

        values = []
        for key in yaml_content:
            values.append({
                "key": key,
                "value": str(yaml_content.get(key))
            })

        return FileValues(file_name, self.type_name, values)
