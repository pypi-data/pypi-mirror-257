from enum import Enum


class GetTagsFieldstagGroupItem(str, Enum):
    DEFAULT = "default"
    EXCLUSIVE = "exclusive"
    NAME = "name"

    def __str__(self) -> str:
        return str(self.value)
