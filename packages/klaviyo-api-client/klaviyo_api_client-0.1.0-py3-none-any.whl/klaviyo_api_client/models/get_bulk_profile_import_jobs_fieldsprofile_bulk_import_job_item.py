from enum import Enum


class GetBulkProfileImportJobsFieldsprofileBulkImportJobItem(str, Enum):
    COMPLETED_AT = "completed_at"
    COMPLETED_COUNT = "completed_count"
    CREATED_AT = "created_at"
    EXPIRES_AT = "expires_at"
    FAILED_COUNT = "failed_count"
    STARTED_AT = "started_at"
    STATUS = "status"
    TOTAL_COUNT = "total_count"

    def __str__(self) -> str:
        return str(self.value)
