from enum import Enum


class EventBulkCreateEnum(str, Enum):
    EVENT_BULK_CREATE = "event-bulk-create"

    def __str__(self) -> str:
        return str(self.value)
