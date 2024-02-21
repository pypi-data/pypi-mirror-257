from enum import Enum


class PatchCouponCodeResponseDataAttributesStatus(str, Enum):
    ASSIGNED_TO_PROFILE = "ASSIGNED_TO_PROFILE"
    DELETING = "DELETING"
    PROCESSING = "PROCESSING"
    UNASSIGNED = "UNASSIGNED"
    VERSION_NOT_ACTIVE = "VERSION_NOT_ACTIVE"

    def __str__(self) -> str:
        return str(self.value)
