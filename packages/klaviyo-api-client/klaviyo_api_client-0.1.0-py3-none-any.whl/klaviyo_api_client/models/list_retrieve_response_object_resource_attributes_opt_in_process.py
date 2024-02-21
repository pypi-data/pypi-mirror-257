from enum import Enum


class ListRetrieveResponseObjectResourceAttributesOptInProcess(str, Enum):
    DOUBLE_OPT_IN = "double_opt_in"
    SINGLE_OPT_IN = "single_opt_in"

    def __str__(self) -> str:
        return str(self.value)
