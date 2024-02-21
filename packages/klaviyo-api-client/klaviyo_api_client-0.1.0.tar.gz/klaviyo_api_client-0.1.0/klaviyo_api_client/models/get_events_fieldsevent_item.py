from enum import Enum


class GetEventsFieldseventItem(str, Enum):
    DATETIME = "datetime"
    EVENT_PROPERTIES = "event_properties"
    TIMESTAMP = "timestamp"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
