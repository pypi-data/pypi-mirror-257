from enum import Enum


class GetEventsSort(str, Enum):
    DATETIME = "datetime"
    TIMESTAMP = "timestamp"
    VALUE_1 = "-datetime"
    VALUE_3 = "-timestamp"

    def __str__(self) -> str:
        return str(self.value)
