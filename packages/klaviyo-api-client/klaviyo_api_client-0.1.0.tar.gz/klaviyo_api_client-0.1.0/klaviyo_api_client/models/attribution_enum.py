from enum import Enum


class AttributionEnum(str, Enum):
    ATTRIBUTION = "attribution"

    def __str__(self) -> str:
        return str(self.value)
