from enum import Enum


class CatalogItemBulkDeleteJobEnum(str, Enum):
    CATALOG_ITEM_BULK_DELETE_JOB = "catalog-item-bulk-delete-job"

    def __str__(self) -> str:
        return str(self.value)
