from enum import Enum


class GetDeleteCategoriesJobsFieldscatalogCategoryBulkDeleteJobItem(str, Enum):
    COMPLETED_AT = "completed_at"
    COMPLETED_COUNT = "completed_count"
    CREATED_AT = "created_at"
    ERRORS = "errors"
    EXPIRES_AT = "expires_at"
    FAILED_COUNT = "failed_count"
    STATUS = "status"
    TOTAL_COUNT = "total_count"

    def __str__(self) -> str:
        return str(self.value)
