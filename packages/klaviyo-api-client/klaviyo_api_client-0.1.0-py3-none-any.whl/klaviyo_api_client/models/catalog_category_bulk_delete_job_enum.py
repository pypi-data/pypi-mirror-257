from enum import Enum


class CatalogCategoryBulkDeleteJobEnum(str, Enum):
    CATALOG_CATEGORY_BULK_DELETE_JOB = "catalog-category-bulk-delete-job"

    def __str__(self) -> str:
        return str(self.value)
