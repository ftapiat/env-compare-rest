import yaml
from abc import ABC

from ..file_values import FileValues
from .file_type_name import FileTypeName
from .file_type import FileType
from .helpers import openshift_list_has_valid_structure, openshift_get_values_from_list


class OcYamlEnvObjFileType(FileType, ABC):
    def __init__(self, content: str):
        file_type = FileTypeName.OC_YAML_ENV_OBJ
        super().__init__(file_type, content)

    def is_valid(self) -> bool:
        """
        Checks if the content is a valid oc yaml env obj file.
        """
        yaml_content = yaml.load(self.content, Loader=yaml.FullLoader)
        if yaml_content is None:
            return False

        if not isinstance(yaml_content, dict):
            return False

        if "env" not in yaml_content:
            return False

        if not isinstance(yaml_content["env"], list):
            return False

        return openshift_list_has_valid_structure(yaml_content["env"])

    def get_values(self, file_name: str) -> FileValues:
        """
        Assumes it's already a valid oc yaml env obj file and returns the values.
        :param file_name:
        :return:
        """
        yaml_content = yaml.load(self.content, Loader=yaml.FullLoader)
        values = openshift_get_values_from_list(yaml_content["env"])
        return FileValues(file_name, self.type_name, values)