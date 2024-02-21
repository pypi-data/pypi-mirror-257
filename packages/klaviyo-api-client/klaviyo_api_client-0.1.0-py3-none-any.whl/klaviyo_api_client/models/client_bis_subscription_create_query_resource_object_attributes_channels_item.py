from enum import Enum


class ClientBISSubscriptionCreateQueryResourceObjectAttributesChannelsItem(str, Enum):
    EMAIL = "EMAIL"
    PUSH = "PUSH"
    SMS = "SMS"

    def __str__(self) -> str:
        return str(self.value)
