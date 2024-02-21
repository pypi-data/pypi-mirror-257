from enum import Enum


class FlowActionEnum(str, Enum):
    FLOW_ACTION = "flow-action"

    def __str__(self) -> str:
        return str(self.value)
