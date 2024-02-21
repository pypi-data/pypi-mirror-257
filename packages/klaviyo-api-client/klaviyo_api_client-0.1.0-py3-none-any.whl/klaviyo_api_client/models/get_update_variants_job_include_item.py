from enum import Enum


class GetUpdateVariantsJobIncludeItem(str, Enum):
    VARIANTS = "variants"

    def __str__(self) -> str:
        return str(self.value)
