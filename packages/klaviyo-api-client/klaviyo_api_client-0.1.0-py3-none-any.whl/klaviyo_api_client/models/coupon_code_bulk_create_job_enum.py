from enum import Enum


class CouponCodeBulkCreateJobEnum(str, Enum):
    COUPON_CODE_BULK_CREATE_JOB = "coupon-code-bulk-create-job"

    def __str__(self) -> str:
        return str(self.value)
