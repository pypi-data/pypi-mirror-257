from enum import Enum


class GetBulkProfileImportJobListsFieldslistItem(str, Enum):
    CREATED = "created"
    NAME = "name"
    OPT_IN_PROCESS = "opt_in_process"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
