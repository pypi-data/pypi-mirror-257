from enum import IntEnum


class PostCatalogVariantResponseDataAttributesInventoryPolicy(IntEnum):
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2

    def __str__(self) -> str:
        return str(self.value)
