from enum import Enum


class GetFlowFieldsflowItem(str, Enum):
    ARCHIVED = "archived"
    CREATED = "created"
    NAME = "name"
    STATUS = "status"
    TRIGGER_TYPE = "trigger_type"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
