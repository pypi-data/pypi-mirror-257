from enum import Enum


class GetTagIncludeItem(str, Enum):
    TAG_GROUP = "tag-group"

    def __str__(self) -> str:
        return str(self.value)
