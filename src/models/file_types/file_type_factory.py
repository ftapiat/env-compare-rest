from .file_type_name import FileTypeName
from .file_type import FileType
from .dotenv_file_type import DotenvFileType
from .oc_yaml_env_obj_file_type import OcYamlEnvObjFileType
from .oc_yaml_env_list_file_type import OcYamlEnvListFileType


class FileTypeFactory:
    @staticmethod
    def from_type(type_name: FileTypeName, content: str) -> FileType:
        if type_name == FileTypeName.DOTENV:
            return DotenvFileType(content)
        elif type_name == FileTypeName.OC_YAML_ENV_OBJ:
            return OcYamlEnvObjFileType(content)
        elif type_name == FileTypeName.OC_YAML_ENV_LIST:
            return OcYamlEnvListFileType(content)
        else:
            raise Exception("Invalid file type.")
