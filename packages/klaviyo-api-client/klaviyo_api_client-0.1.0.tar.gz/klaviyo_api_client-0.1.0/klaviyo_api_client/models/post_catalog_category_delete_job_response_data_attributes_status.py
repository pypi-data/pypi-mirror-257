from enum import Enum


class PostCatalogCategoryDeleteJobResponseDataAttributesStatus(str, Enum):
    CANCELLED = "cancelled"
    COMPLETE = "complete"
    PROCESSING = "processing"
    QUEUED = "queued"

    def __str__(self) -> str:
        return str(self.value)
