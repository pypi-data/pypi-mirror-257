from enum import Enum


class CatalogVariantBulkCreateJobEnum(str, Enum):
    CATALOG_VARIANT_BULK_CREATE_JOB = "catalog-variant-bulk-create-job"

    def __str__(self) -> str:
        return str(self.value)
