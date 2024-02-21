from enum import Enum


class GetImagesSort(str, Enum):
    FORMAT = "format"
    ID = "id"
    NAME = "name"
    SIZE = "size"
    UPDATED_AT = "updated_at"
    VALUE_1 = "-format"
    VALUE_3 = "-id"
    VALUE_5 = "-name"
    VALUE_7 = "-size"
    VALUE_9 = "-updated_at"

    def __str__(self) -> str:
        return str(self.value)
