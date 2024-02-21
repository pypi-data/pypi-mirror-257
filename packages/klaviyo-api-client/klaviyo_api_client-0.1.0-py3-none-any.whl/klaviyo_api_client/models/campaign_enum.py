from enum import Enum


class CampaignEnum(str, Enum):
    CAMPAIGN = "campaign"

    def __str__(self) -> str:
        return str(self.value)
