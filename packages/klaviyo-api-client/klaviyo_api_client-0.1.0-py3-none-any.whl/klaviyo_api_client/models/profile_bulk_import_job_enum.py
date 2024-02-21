from enum import Enum


class ProfileBulkImportJobEnum(str, Enum):
    PROFILE_BULK_IMPORT_JOB = "profile-bulk-import-job"

    def __str__(self) -> str:
        return str(self.value)
