from enum import Enum


class CatalogCategoryBulkCreateJobEnum(str, Enum):
    CATALOG_CATEGORY_BULK_CREATE_JOB = "catalog-category-bulk-create-job"

    def __str__(self) -> str:
        return str(self.value)
