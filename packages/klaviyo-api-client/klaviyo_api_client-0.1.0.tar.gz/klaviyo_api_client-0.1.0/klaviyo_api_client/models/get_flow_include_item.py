from enum import Enum


class GetFlowIncludeItem(str, Enum):
    FLOW_ACTIONS = "flow-actions"
    TAGS = "tags"

    def __str__(self) -> str:
        return str(self.value)
