from enum import Enum


class FlowEnum(str, Enum):
    FLOW = "flow"

    def __str__(self) -> str:
        return str(self.value)
