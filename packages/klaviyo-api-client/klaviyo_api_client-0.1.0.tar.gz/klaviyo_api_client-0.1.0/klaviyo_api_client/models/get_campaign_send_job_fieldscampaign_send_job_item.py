from enum import Enum


class GetCampaignSendJobFieldscampaignSendJobItem(str, Enum):
    STATUS = "status"

    def __str__(self) -> str:
        return str(self.value)
