from enum import Enum


class FlowValuesReportEnum(str, Enum):
    FLOW_VALUES_REPORT = "flow-values-report"

    def __str__(self) -> str:
        return str(self.value)
