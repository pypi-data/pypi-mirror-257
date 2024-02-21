from enum import Enum


class ProfileSubscriptionBulkCreateJobEnum(str, Enum):
    PROFILE_SUBSCRIPTION_BULK_CREATE_JOB = "profile-subscription-bulk-create-job"

    def __str__(self) -> str:
        return str(self.value)
