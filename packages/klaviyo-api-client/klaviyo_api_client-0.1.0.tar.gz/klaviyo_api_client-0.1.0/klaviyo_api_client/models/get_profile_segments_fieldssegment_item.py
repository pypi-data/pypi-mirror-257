from enum import Enum


class GetProfileSegmentsFieldssegmentItem(str, Enum):
    CREATED = "created"
    NAME = "name"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
