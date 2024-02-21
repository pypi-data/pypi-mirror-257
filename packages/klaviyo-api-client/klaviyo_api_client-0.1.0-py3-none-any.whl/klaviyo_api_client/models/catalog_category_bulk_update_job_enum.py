from enum import Enum


class CatalogCategoryBulkUpdateJobEnum(str, Enum):
    CATALOG_CATEGORY_BULK_UPDATE_JOB = "catalog-category-bulk-update-job"

    def __str__(self) -> str:
        return str(self.value)
