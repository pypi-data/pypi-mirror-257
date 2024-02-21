from enum import Enum


class MetricEnum(str, Enum):
    METRIC = "metric"

    def __str__(self) -> str:
        return str(self.value)
