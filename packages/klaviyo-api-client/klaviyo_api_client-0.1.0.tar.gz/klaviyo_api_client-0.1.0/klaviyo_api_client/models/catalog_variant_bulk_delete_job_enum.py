from enum import Enum


class CatalogVariantBulkDeleteJobEnum(str, Enum):
    CATALOG_VARIANT_BULK_DELETE_JOB = "catalog-variant-bulk-delete-job"

    def __str__(self) -> str:
        return str(self.value)
