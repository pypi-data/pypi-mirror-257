from enum import Enum


class DataPrivacyDeletionJobEnum(str, Enum):
    DATA_PRIVACY_DELETION_JOB = "data-privacy-deletion-job"

    def __str__(self) -> str:
        return str(self.value)
