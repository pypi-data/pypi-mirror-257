from enum import Enum


class ServerBISSubscriptionCreateQueryResourceObjectAttributesChannelsItem(str, Enum):
    EMAIL = "EMAIL"
    PUSH = "PUSH"
    SMS = "SMS"

    def __str__(self) -> str:
        return str(self.value)
