from enum import Enum


class GetCatalogItemIncludeItem(str, Enum):
    VARIANTS = "variants"

    def __str__(self) -> str:
        return str(self.value)
