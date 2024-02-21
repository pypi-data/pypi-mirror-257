from enum import Enum


class GetCouponCodeFieldscouponItem(str, Enum):
    DESCRIPTION = "description"
    EXTERNAL_ID = "external_id"

    def __str__(self) -> str:
        return str(self.value)
