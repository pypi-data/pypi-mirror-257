from enum import Enum


class PushTokenEnum(str, Enum):
    PUSH_TOKEN = "push-token"

    def __str__(self) -> str:
        return str(self.value)
