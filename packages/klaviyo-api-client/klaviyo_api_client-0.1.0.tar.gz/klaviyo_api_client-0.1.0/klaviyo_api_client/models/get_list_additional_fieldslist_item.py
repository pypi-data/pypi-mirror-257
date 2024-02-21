from enum import Enum


class GetListAdditionalFieldslistItem(str, Enum):
    PROFILE_COUNT = "profile_count"

    def __str__(self) -> str:
        return str(self.value)
