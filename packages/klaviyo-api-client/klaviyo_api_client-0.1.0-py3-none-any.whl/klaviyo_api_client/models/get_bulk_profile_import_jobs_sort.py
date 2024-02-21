from enum import Enum


class GetBulkProfileImportJobsSort(str, Enum):
    CREATED_AT = "created_at"
    VALUE_1 = "-created_at"

    def __str__(self) -> str:
        return str(self.value)
