from enum import Enum


class FlowValuesRequestDTOResourceObjectAttributesStatisticsItem(str, Enum):
    AVERAGE_ORDER_VALUE = "average_order_value"
    BOUNCED = "bounced"
    BOUNCED_OR_FAILED = "bounced_or_failed"
    BOUNCED_OR_FAILED_RATE = "bounced_or_failed_rate"
    BOUNCE_RATE = "bounce_rate"
    CLICKS = "clicks"
    CLICKS_UNIQUE = "clicks_unique"
    CLICK_RATE = "click_rate"
    CLICK_TO_OPEN_RATE = "click_to_open_rate"
    CONVERSIONS = "conversions"
    CONVERSION_RATE = "conversion_rate"
    CONVERSION_UNIQUES = "conversion_uniques"
    CONVERSION_VALUE = "conversion_value"
    DELIVERED = "delivered"
    DELIVERY_RATE = "delivery_rate"
    FAILED = "failed"
    FAILED_RATE = "failed_rate"
    OPENS = "opens"
    OPENS_UNIQUE = "opens_unique"
    OPEN_RATE = "open_rate"
    RECIPIENTS = "recipients"
    REVENUE_PER_RECIPIENT = "revenue_per_recipient"
    SPAM_COMPLAINTS = "spam_complaints"
    SPAM_COMPLAINT_RATE = "spam_complaint_rate"
    UNSUBSCRIBES = "unsubscribes"
    UNSUBSCRIBE_RATE = "unsubscribe_rate"
    UNSUBSCRIBE_UNIQUES = "unsubscribe_uniques"

    def __str__(self) -> str:
        return str(self.value)
