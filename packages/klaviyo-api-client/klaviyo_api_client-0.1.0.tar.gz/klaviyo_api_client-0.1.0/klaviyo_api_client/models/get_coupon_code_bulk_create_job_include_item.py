from enum import Enum


class GetCouponCodeBulkCreateJobIncludeItem(str, Enum):
    COUPON_CODES = "coupon-codes"

    def __str__(self) -> str:
        return str(self.value)
