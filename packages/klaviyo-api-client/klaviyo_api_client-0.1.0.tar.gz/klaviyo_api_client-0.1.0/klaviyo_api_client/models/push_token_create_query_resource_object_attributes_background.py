from enum import Enum


class PushTokenCreateQueryResourceObjectAttributesBackground(str, Enum):
    AVAILABLE = "AVAILABLE"
    DENIED = "DENIED"
    RESTRICTED = "RESTRICTED"

    def __str__(self) -> str:
        return str(self.value)
