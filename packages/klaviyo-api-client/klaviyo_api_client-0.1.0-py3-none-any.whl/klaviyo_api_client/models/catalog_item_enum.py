from enum import Enum


class CatalogItemEnum(str, Enum):
    CATALOG_ITEM = "catalog-item"

    def __str__(self) -> str:
        return str(self.value)
