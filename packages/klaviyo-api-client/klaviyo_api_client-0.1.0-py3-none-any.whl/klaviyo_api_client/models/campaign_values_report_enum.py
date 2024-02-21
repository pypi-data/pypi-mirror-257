from enum import Enum


class CampaignValuesReportEnum(str, Enum):
    CAMPAIGN_VALUES_REPORT = "campaign-values-report"

    def __str__(self) -> str:
        return str(self.value)
