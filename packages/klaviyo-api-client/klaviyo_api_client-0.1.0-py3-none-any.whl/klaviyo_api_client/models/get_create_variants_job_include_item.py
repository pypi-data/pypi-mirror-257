from enum import Enum


class GetCreateVariantsJobIncludeItem(str, Enum):
    VARIANTS = "variants"

    def __str__(self) -> str:
        return str(self.value)
