from enum import Enum


class GetBulkProfileImportJobImportErrorsFieldsimportErrorItem(str, Enum):
    CODE = "code"
    DETAIL = "detail"
    ORIGINAL_PAYLOAD = "original_payload"
    SOURCE = "source"
    SOURCE_POINTER = "source.pointer"
    TITLE = "title"

    def __str__(self) -> str:
        return str(self.value)
