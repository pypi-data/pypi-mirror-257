from enum import Enum


class CatalogVariantBulkUpdateJobEnum(str, Enum):
    CATALOG_VARIANT_BULK_UPDATE_JOB = "catalog-variant-bulk-update-job"

    def __str__(self) -> str:
        return str(self.value)
