from enum import Enum


class DeviceMetadataOsName(str, Enum):
    ANDROID = "android"
    IOS = "ios"
    IPADOS = "ipados"
    MACOS = "macos"
    TVOS = "tvos"

    def __str__(self) -> str:
        return str(self.value)
