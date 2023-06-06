from enum import Enum


class FileTypeName(Enum):
    DOTENV = "dotenv"
    OC_YAML_ENV = "openshift-yaml-env"
    OC_YAML_CONFIGMAP = "openshift-yaml-configmap"
    NONE = None

    @classmethod
    def available_list(cls):
        return list(filter(lambda c: c != cls.NONE.value, cls.list()))

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
