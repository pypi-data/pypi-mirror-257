from enum import Enum


class GetProfileIncludeItem(str, Enum):
    LISTS = "lists"
    SEGMENTS = "segments"

    def __str__(self) -> str:
        return str(self.value)
