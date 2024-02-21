from enum import Enum


class GetCatalogItemCategoriesSort(str, Enum):
    CREATED = "created"
    VALUE_1 = "-created"

    def __str__(self) -> str:
        return str(self.value)
