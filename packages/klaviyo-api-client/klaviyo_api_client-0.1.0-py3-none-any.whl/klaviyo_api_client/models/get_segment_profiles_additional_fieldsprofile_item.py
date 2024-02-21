from enum import Enum


class GetSegmentProfilesAdditionalFieldsprofileItem(str, Enum):
    PREDICTIVE_ANALYTICS = "predictive_analytics"
    SUBSCRIPTIONS = "subscriptions"

    def __str__(self) -> str:
        return str(self.value)
