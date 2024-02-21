from enum import Enum


class GetCatalogCategoryItemsIncludeItem(str, Enum):
    VARIANTS = "variants"

    def __str__(self) -> str:
        return str(self.value)
