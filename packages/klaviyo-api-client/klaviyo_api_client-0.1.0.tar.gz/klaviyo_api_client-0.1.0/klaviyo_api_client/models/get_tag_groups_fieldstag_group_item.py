from enum import Enum


class GetTagGroupsFieldstagGroupItem(str, Enum):
    DEFAULT = "default"
    EXCLUSIVE = "exclusive"
    NAME = "name"

    def __str__(self) -> str:
        return str(self.value)
