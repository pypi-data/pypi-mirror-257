from enum import Enum


class ProfileSubscriptionBulkDeleteJobEnum(str, Enum):
    PROFILE_SUBSCRIPTION_BULK_DELETE_JOB = "profile-subscription-bulk-delete-job"

    def __str__(self) -> str:
        return str(self.value)
