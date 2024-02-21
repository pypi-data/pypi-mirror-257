from enum import Enum


class GetSegmentFieldssegmentItem(str, Enum):
    CREATED = "created"
    NAME = "name"
    PROFILE_COUNT = "profile_count"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
