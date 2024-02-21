from enum import Enum


class MarketingSubscriptionParametersConsent(str, Enum):
    SUBSCRIBED = "SUBSCRIBED"

    def __str__(self) -> str:
        return str(self.value)
