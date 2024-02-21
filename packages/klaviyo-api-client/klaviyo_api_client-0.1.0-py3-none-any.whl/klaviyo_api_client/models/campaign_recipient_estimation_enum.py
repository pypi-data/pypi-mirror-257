from enum import Enum


class CampaignRecipientEstimationEnum(str, Enum):
    CAMPAIGN_RECIPIENT_ESTIMATION = "campaign-recipient-estimation"

    def __str__(self) -> str:
        return str(self.value)
