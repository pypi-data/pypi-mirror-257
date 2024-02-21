from enum import Enum


class ProfileMergeEnum(str, Enum):
    PROFILE_MERGE = "profile-merge"

    def __str__(self) -> str:
        return str(self.value)
