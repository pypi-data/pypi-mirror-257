from enum import Enum


class GetEventFieldseventItem(str, Enum):
    DATETIME = "datetime"
    EVENT_PROPERTIES = "event_properties"
    TIMESTAMP = "timestamp"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
