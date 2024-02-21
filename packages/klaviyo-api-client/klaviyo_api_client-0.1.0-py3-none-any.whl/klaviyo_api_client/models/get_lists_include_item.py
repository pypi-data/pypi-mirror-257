from enum import Enum


class GetListsIncludeItem(str, Enum):
    TAGS = "tags"

    def __str__(self) -> str:
        return str(self.value)
