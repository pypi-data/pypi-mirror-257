from enum import Enum


class GetCouponCodesIncludeItem(str, Enum):
    COUPON = "coupon"

    def __str__(self) -> str:
        return str(self.value)
