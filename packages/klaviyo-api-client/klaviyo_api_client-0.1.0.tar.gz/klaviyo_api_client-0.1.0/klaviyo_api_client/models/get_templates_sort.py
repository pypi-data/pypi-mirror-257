from enum import Enum


class GetTemplatesSort(str, Enum):
    CREATED = "created"
    ID = "id"
    NAME = "name"
    UPDATED = "updated"
    VALUE_1 = "-created"
    VALUE_3 = "-id"
    VALUE_5 = "-name"
    VALUE_7 = "-updated"

    def __str__(self) -> str:
        return str(self.value)
