from enum import Enum


class GetTagGroupsSort(str, Enum):
    ID = "id"
    NAME = "name"
    VALUE_1 = "-id"
    VALUE_3 = "-name"

    def __str__(self) -> str:
        return str(self.value)
