from enum import Enum


class GetCreateItemsJobIncludeItem(str, Enum):
    ITEMS = "items"

    def __str__(self) -> str:
        return str(self.value)
