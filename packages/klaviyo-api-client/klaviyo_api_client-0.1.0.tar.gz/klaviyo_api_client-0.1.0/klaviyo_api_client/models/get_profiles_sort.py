from enum import Enum


class GetProfilesSort(str, Enum):
    CREATED = "created"
    EMAIL = "email"
    ID = "id"
    SUBSCRIPTIONS_EMAIL_MARKETING_LIST_SUPPRESSIONS_TIMESTAMP = (
        "subscriptions.email.marketing.list_suppressions.timestamp"
    )
    SUBSCRIPTIONS_EMAIL_MARKETING_SUPPRESSION_TIMESTAMP = "subscriptions.email.marketing.suppression.timestamp"
    UPDATED = "updated"
    VALUE_1 = "-created"
    VALUE_11 = "-subscriptions.email.marketing.suppression.timestamp"
    VALUE_3 = "-email"
    VALUE_5 = "-id"
    VALUE_7 = "-updated"
    VALUE_9 = "-subscriptions.email.marketing.list_suppressions.timestamp"

    def __str__(self) -> str:
        return str(self.value)
