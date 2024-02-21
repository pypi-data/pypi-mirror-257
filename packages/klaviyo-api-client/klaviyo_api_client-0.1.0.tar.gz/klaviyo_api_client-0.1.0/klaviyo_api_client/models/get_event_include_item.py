from enum import Enum


class GetEventIncludeItem(str, Enum):
    ATTRIBUTIONS = "attributions"
    METRIC = "metric"
    PROFILE = "profile"

    def __str__(self) -> str:
        return str(self.value)
