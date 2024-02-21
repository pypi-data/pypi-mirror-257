from enum import Enum


class CatalogItemBulkCreateJobEnum(str, Enum):
    CATALOG_ITEM_BULK_CREATE_JOB = "catalog-item-bulk-create-job"

    def __str__(self) -> str:
        return str(self.value)
