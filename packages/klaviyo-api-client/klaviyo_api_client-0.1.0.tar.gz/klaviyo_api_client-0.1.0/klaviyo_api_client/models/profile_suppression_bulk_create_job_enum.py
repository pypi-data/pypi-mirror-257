from enum import Enum


class ProfileSuppressionBulkCreateJobEnum(str, Enum):
    PROFILE_SUPPRESSION_BULK_CREATE_JOB = "profile-suppression-bulk-create-job"

    def __str__(self) -> str:
        return str(self.value)
