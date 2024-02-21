from enum import Enum


class CampaignSendJobEnum(str, Enum):
    CAMPAIGN_SEND_JOB = "campaign-send-job"

    def __str__(self) -> str:
        return str(self.value)
