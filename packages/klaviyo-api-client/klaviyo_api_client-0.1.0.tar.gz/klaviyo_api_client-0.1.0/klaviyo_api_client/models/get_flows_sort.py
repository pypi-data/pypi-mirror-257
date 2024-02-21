from enum import Enum


class GetFlowsSort(str, Enum):
    CREATED = "created"
    ID = "id"
    NAME = "name"
    STATUS = "status"
    TRIGGER_TYPE = "trigger_type"
    UPDATED = "updated"
    VALUE_1 = "-created"
    VALUE_11 = "-updated"
    VALUE_3 = "-id"
    VALUE_5 = "-name"
    VALUE_7 = "-status"
    VALUE_9 = "-trigger_type"

    def __str__(self) -> str:
        return str(self.value)
