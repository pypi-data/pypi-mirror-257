from enum import Enum


class GetFlowMessageFieldstemplateItem(str, Enum):
    CREATED = "created"
    EDITOR_TYPE = "editor_type"
    HTML = "html"
    NAME = "name"
    TEXT = "text"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
