from enum import Enum


class PushTokenCreateQueryResourceObjectAttributesPlatform(str, Enum):
    ANDROID = "android"
    IOS = "ios"

    def __str__(self) -> str:
        return str(self.value)
