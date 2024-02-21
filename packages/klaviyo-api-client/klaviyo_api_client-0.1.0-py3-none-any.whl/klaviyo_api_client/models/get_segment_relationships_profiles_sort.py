from enum import Enum


class GetSegmentRelationshipsProfilesSort(str, Enum):
    JOINED_GROUP_AT = "joined_group_at"
    VALUE_1 = "-joined_group_at"

    def __str__(self) -> str:
        return str(self.value)
