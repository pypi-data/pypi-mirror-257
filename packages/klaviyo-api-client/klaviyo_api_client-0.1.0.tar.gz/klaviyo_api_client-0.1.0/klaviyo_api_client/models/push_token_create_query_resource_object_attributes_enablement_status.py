from enum import Enum


class PushTokenCreateQueryResourceObjectAttributesEnablementStatus(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    DENIED = "DENIED"
    NOT_DETERMINED = "NOT_DETERMINED"
    PROVISIONAL = "PROVISIONAL"
    UNAUTHORIZED = "UNAUTHORIZED"

    def __str__(self) -> str:
        return str(self.value)
