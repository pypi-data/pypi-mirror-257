from enum import Enum


class CouponCodeEnum(str, Enum):
    COUPON_CODE = "coupon-code"

    def __str__(self) -> str:
        return str(self.value)
