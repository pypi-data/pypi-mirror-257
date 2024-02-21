from enum import Enum


class GetFlowActionIncludeItem(str, Enum):
    FLOW = "flow"
    FLOW_MESSAGES = "flow-messages"

    def __str__(self) -> str:
        return str(self.value)
