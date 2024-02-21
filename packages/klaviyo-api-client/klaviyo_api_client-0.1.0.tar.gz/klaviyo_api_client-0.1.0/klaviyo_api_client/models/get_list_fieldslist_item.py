from enum import Enum


class GetListFieldslistItem(str, Enum):
    CREATED = "created"
    NAME = "name"
    OPT_IN_PROCESS = "opt_in_process"
    PROFILE_COUNT = "profile_count"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
