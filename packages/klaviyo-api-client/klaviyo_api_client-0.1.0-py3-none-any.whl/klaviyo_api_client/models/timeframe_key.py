from enum import Enum


class TimeframeKey(str, Enum):
    LAST_12_MONTHS = "last_12_months"
    LAST_30_DAYS = "last_30_days"
    LAST_365_DAYS = "last_365_days"
    LAST_3_MONTHS = "last_3_months"
    LAST_7_DAYS = "last_7_days"
    LAST_90_DAYS = "last_90_days"
    LAST_MONTH = "last_month"
    LAST_WEEK = "last_week"
    LAST_YEAR = "last_year"
    THIS_MONTH = "this_month"
    THIS_WEEK = "this_week"
    THIS_YEAR = "this_year"
    TODAY = "today"
    YESTERDAY = "yesterday"

    def __str__(self) -> str:
        return str(self.value)
