from enum import Enum


class GetFlowFlowActionsSort(str, Enum):
    ACTION_TYPE = "action_type"
    CREATED = "created"
    ID = "id"
    STATUS = "status"
    UPDATED = "updated"
    VALUE_1 = "-action_type"
    VALUE_3 = "-created"
    VALUE_5 = "-id"
    VALUE_7 = "-status"
    VALUE_9 = "-updated"

    def __str__(self) -> str:
        return str(self.value)
