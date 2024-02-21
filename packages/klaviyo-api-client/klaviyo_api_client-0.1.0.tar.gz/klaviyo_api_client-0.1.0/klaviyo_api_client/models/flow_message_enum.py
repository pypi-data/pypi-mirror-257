from enum import Enum


class FlowMessageEnum(str, Enum):
    FLOW_MESSAGE = "flow-message"

    def __str__(self) -> str:
        return str(self.value)
