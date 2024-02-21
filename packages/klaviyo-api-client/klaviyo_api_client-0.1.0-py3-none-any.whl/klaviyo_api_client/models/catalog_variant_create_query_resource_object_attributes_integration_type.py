from enum import Enum


class CatalogVariantCreateQueryResourceObjectAttributesIntegrationType(str, Enum):
    VALUE_0 = "$custom"

    def __str__(self) -> str:
        return str(self.value)
