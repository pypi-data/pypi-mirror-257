from enum import Enum


class GetCouponCodeIncludeItem(str, Enum):
    COUPON = "coupon"

    def __str__(self) -> str:
        return str(self.value)
