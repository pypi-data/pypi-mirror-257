from enum import Enum


class CatalogItemBulkUpdateJobEnum(str, Enum):
    CATALOG_ITEM_BULK_UPDATE_JOB = "catalog-item-bulk-update-job"

    def __str__(self) -> str:
        return str(self.value)
