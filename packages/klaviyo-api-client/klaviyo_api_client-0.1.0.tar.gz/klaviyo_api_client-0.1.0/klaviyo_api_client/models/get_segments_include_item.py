from enum import Enum


class GetSegmentsIncludeItem(str, Enum):
    TAGS = "tags"

    def __str__(self) -> str:
        return str(self.value)
