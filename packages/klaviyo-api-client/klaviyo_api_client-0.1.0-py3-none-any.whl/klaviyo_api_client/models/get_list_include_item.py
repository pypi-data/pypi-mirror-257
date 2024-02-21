from enum import Enum


class GetListIncludeItem(str, Enum):
    TAGS = "tags"

    def __str__(self) -> str:
        return str(self.value)
