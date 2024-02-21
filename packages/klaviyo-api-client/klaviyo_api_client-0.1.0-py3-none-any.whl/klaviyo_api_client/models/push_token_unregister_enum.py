from enum import Enum


class PushTokenUnregisterEnum(str, Enum):
    PUSH_TOKEN_UNREGISTER = "push-token-unregister"

    def __str__(self) -> str:
        return str(self.value)
