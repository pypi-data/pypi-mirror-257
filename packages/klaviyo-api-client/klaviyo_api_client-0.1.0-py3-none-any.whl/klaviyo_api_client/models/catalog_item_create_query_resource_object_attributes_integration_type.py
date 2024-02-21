from enum import Enum


class CatalogItemCreateQueryResourceObjectAttributesIntegrationType(str, Enum):
    VALUE_0 = "$custom"

    def __str__(self) -> str:
        return str(self.value)
