from enum import Enum


class FlowSeriesReportEnum(str, Enum):
    FLOW_SERIES_REPORT = "flow-series-report"

    def __str__(self) -> str:
        return str(self.value)
