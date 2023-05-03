from enum import Enum


class FileTypeEnum(Enum):
    DOTENV = "dotenv"
    OC_YAML_ENV_OBJ = "openshift-yaml-env-object"
    OC_YAML_ENV_LIST = "openshift-yaml-env-list"
    NONE = None
