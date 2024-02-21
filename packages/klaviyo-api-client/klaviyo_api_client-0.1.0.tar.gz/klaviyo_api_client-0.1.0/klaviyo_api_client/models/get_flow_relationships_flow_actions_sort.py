from enum import Enum


class GetFlowRelationshipsFlowActionsSort(str, Enum):
    CREATED = "created"
    ID = "id"
    STATUS = "status"
    UPDATED = "updated"
    VALUE_1 = "-created"
    VALUE_3 = "-id"
    VALUE_5 = "-status"
    VALUE_7 = "-updated"

    def __str__(self) -> str:
        return str(self.value)
