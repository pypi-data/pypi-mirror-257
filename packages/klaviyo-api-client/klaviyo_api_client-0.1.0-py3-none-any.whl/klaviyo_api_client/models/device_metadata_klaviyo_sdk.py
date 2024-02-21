from enum import Enum


class DeviceMetadataKlaviyoSdk(str, Enum):
    ANDROID = "android"
    SWIFT = "swift"

    def __str__(self) -> str:
        return str(self.value)
