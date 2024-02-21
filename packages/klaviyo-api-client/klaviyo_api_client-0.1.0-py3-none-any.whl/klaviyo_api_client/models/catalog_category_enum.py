from enum import Enum


class CatalogCategoryEnum(str, Enum):
    CATALOG_CATEGORY = "catalog-category"

    def __str__(self) -> str:
        return str(self.value)
