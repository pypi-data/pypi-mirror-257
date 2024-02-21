from enum import Enum


class MetricAggregateEnum(str, Enum):
    METRIC_AGGREGATE = "metric-aggregate"

    def __str__(self) -> str:
        return str(self.value)
