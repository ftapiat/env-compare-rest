from .file_type_name import FileTypeName
from .file_type import FileType
from .dotenv_file_type import DotenvFileType
from .oc_yaml_env_file_type import OcYamlEnvFileType
from .oc_yaml_configmap_file_type import OcYamlConfigmapFileType
from .file_type_invalid_exception import FileTypeInvalidException


class FileTypeFactory:
    @staticmethod
    def from_type(type_name: FileTypeName, content: str) -> FileType:
        if type_name == FileTypeName.DOTENV:
            return DotenvFileType(content)
        elif type_name == FileTypeName.OC_YAML_ENV:
            return OcYamlEnvFileType(content)
        elif type_name == FileTypeName.OC_YAML_CONFIGMAP:
            return OcYamlConfigmapFileType(content)
        else:
            raise FileTypeInvalidException()
