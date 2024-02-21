from enum import Enum


class SegmentEnum(str, Enum):
    SEGMENT = "segment"

    def __str__(self) -> str:
        return str(self.value)
