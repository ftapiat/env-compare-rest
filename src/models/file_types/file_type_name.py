from enum import Enum


class FileTypeName(Enum):
    DOTENV = "dotenv"
    OC_YAML_ENV_OBJ = "openshift-yaml-env-object"
    OC_YAML_ENV_LIST = "openshift-yaml-env-list"
    OC_YAML_CONFIGMAP = "openshift-yaml-configmap"
    NONE = None
