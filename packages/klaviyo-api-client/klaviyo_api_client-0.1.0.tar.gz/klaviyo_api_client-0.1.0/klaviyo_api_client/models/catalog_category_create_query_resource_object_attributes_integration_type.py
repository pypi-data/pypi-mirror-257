from enum import Enum


class CatalogCategoryCreateQueryResourceObjectAttributesIntegrationType(str, Enum):
    VALUE_0 = "$custom"

    def __str__(self) -> str:
        return str(self.value)
