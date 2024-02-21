from enum import Enum


class TagGroupEnum(str, Enum):
    TAG_GROUP = "tag-group"

    def __str__(self) -> str:
        return str(self.value)
