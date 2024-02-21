from enum import Enum


class GetProfileFieldssegmentItem(str, Enum):
    CREATED = "created"
    NAME = "name"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
