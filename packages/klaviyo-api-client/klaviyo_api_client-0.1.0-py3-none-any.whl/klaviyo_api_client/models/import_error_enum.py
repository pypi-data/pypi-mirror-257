from enum import Enum


class ImportErrorEnum(str, Enum):
    IMPORT_ERROR = "import-error"

    def __str__(self) -> str:
        return str(self.value)
