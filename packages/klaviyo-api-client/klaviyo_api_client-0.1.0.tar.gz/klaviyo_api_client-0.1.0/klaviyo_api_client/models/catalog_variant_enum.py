from enum import Enum


class CatalogVariantEnum(str, Enum):
    CATALOG_VARIANT = "catalog-variant"

    def __str__(self) -> str:
        return str(self.value)
