from enum import Enum


class CampaignRecipientEstimationJobEnum(str, Enum):
    CAMPAIGN_RECIPIENT_ESTIMATION_JOB = "campaign-recipient-estimation-job"

    def __str__(self) -> str:
        return str(self.value)
