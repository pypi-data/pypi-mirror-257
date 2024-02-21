from enum import Enum


class GetTagsSort(str, Enum):
    ID = "id"
    NAME = "name"
    VALUE_1 = "-id"
    VALUE_3 = "-name"

    def __str__(self) -> str:
        return str(self.value)
