from enum import Enum


class GetCampaignRecipientEstimationFieldscampaignRecipientEstimationItem(str, Enum):
    ESTIMATED_RECIPIENT_COUNT = "estimated_recipient_count"

    def __str__(self) -> str:
        return str(self.value)
