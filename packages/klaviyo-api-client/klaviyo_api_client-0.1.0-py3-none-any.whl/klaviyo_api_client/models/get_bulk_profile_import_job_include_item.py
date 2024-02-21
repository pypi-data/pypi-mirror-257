from enum import Enum


class GetBulkProfileImportJobIncludeItem(str, Enum):
    LISTS = "lists"

    def __str__(self) -> str:
        return str(self.value)
