from enum import Enum


class CampaignMessageEnum(str, Enum):
    CAMPAIGN_MESSAGE = "campaign-message"

    def __str__(self) -> str:
        return str(self.value)
