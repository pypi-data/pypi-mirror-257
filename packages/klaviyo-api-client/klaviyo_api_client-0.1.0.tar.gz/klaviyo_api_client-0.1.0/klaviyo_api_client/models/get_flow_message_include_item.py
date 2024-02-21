from enum import Enum


class GetFlowMessageIncludeItem(str, Enum):
    FLOW_ACTION = "flow-action"
    TEMPLATE = "template"

    def __str__(self) -> str:
        return str(self.value)
