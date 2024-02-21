from enum import Enum


class GetCampaignsIncludeItem(str, Enum):
    CAMPAIGN_MESSAGES = "campaign-messages"
    TAGS = "tags"

    def __str__(self) -> str:
        return str(self.value)
