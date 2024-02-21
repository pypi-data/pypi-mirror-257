from enum import Enum


class GetCampaignMessageFieldstemplateItem(str, Enum):
    CREATED = "created"
    EDITOR_TYPE = "editor_type"
    HTML = "html"
    NAME = "name"
    TEXT = "text"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
