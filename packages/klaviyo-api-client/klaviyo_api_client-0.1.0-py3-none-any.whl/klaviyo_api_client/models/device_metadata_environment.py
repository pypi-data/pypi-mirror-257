from enum import Enum


class DeviceMetadataEnvironment(str, Enum):
    DEBUG = "debug"
    RELEASE = "release"

    def __str__(self) -> str:
        return str(self.value)
