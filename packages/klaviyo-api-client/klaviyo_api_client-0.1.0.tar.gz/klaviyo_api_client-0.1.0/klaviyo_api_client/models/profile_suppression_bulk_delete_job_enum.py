from enum import Enum


class ProfileSuppressionBulkDeleteJobEnum(str, Enum):
    PROFILE_SUPPRESSION_BULK_DELETE_JOB = "profile-suppression-bulk-delete-job"

    def __str__(self) -> str:
        return str(self.value)
