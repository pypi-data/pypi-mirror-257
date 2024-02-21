from enum import Enum


class EventEnum(str, Enum):
    EVENT = "event"

    def __str__(self) -> str:
        return str(self.value)
