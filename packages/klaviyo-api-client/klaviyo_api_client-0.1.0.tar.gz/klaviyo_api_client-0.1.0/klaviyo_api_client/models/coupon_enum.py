from enum import Enum


class CouponEnum(str, Enum):
    COUPON = "coupon"

    def __str__(self) -> str:
        return str(self.value)
