from enum import Enum


class GetFlowsIncludeItem(str, Enum):
    FLOW_ACTIONS = "flow-actions"
    TAGS = "tags"

    def __str__(self) -> str:
        return str(self.value)
