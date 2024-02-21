from enum import Enum


class MetricAggregateQueryResourceObjectAttributesMeasurementsItem(str, Enum):
    COUNT = "count"
    SUM_VALUE = "sum_value"
    UNIQUE = "unique"

    def __str__(self) -> str:
        return str(self.value)
