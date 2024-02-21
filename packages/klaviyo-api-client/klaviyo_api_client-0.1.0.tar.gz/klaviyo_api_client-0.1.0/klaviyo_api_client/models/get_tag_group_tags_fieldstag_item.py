from enum import Enum


class GetTagGroupTagsFieldstagItem(str, Enum):
    NAME = "name"

    def __str__(self) -> str:
        return str(self.value)
