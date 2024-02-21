from enum import Enum


class GetUpdateItemsJobIncludeItem(str, Enum):
    ITEMS = "items"

    def __str__(self) -> str:
        return str(self.value)
