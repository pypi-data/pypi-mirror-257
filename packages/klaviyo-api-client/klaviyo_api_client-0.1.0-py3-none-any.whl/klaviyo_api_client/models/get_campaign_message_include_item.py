from enum import Enum


class GetCampaignMessageIncludeItem(str, Enum):
    CAMPAIGN = "campaign"
    TEMPLATE = "template"

    def __str__(self) -> str:
        return str(self.value)
